import asyncio
import hashlib
import hmac
import mimetypes
import re
import urllib.parse
import urllib.request
from dataclasses import dataclass
from datetime import UTC, datetime

from app.core.config import settings

_SAFE_FILENAME = re.compile(r"[^A-Za-z0-9._-]+")


@dataclass(frozen=True)
class RemoteFile:
    body: bytes
    content_type: str
    filename: str


class S3ImageStorage:
    def __init__(
        self,
        bucket: str | None = settings.aws_bucket,
        region: str = settings.aws_region,
        access_key_id: str | None = settings.aws_access_key_id,
        secret_access_key: str | None = settings.aws_secret_access_key,
    ) -> None:
        self.bucket = bucket
        self.region = region
        self.access_key_id = access_key_id
        self.secret_access_key = secret_access_key

    @property
    def configured(self) -> bool:
        return bool(self.bucket and self.access_key_id and self.secret_access_key)

    async def upload_from_url(
        self,
        source_url: str,
        user_id: str,
        interest_item_id: str,
    ) -> str:
        if not self.configured:
            return source_url

        remote_file = await asyncio.to_thread(self._read_remote_file, source_url)
        key = f"interest-items/{user_id}/{interest_item_id}/{remote_file.filename}"
        await asyncio.to_thread(
            self._put_object,
            key,
            remote_file.body,
            remote_file.content_type,
        )
        return self._public_url(key)

    def _read_remote_file(self, source_url: str) -> RemoteFile:
        request = urllib.request.Request(
            source_url,
            headers={"User-Agent": "blanker-api/1.0"},
        )
        with urllib.request.urlopen(request, timeout=20) as response:
            body = response.read()
            content_type = response.headers.get_content_type()

        return RemoteFile(
            body=body,
            content_type=content_type,
            filename=self._filename(source_url, content_type),
        )

    def _filename(self, source_url: str, content_type: str) -> str:
        parsed_url = urllib.parse.urlparse(source_url)
        if parsed_url.scheme == "data":
            extension = mimetypes.guess_extension(content_type) or ".png"
            return f"image{extension}"

        path = parsed_url.path
        filename = _SAFE_FILENAME.sub("-", path.rsplit("/", 1)[-1]).strip(".-")
        if filename:
            return filename

        extension = mimetypes.guess_extension(content_type) or ".png"
        return f"image{extension}"

    def _put_object(self, key: str, body: bytes, content_type: str) -> None:
        assert self.bucket is not None
        assert self.access_key_id is not None
        assert self.secret_access_key is not None

        host = f"{self.bucket}.s3.{self.region}.amazonaws.com"
        encoded_key = "/".join(urllib.parse.quote(part) for part in key.split("/"))
        url = f"https://{host}/{encoded_key}"
        payload_hash = hashlib.sha256(body).hexdigest()
        now = datetime.now(UTC)
        amz_date = now.strftime("%Y%m%dT%H%M%SZ")
        date_stamp = now.strftime("%Y%m%d")
        headers = {
            "Content-Type": content_type,
            "Host": host,
            "X-Amz-Content-Sha256": payload_hash,
            "X-Amz-Date": amz_date,
        }
        headers["Authorization"] = self._authorization(
            method="PUT",
            canonical_uri=f"/{encoded_key}",
            headers=headers,
            payload_hash=payload_hash,
            amz_date=amz_date,
            date_stamp=date_stamp,
        )
        request = urllib.request.Request(
            url,
            data=body,
            headers=headers,
            method="PUT",
        )
        with urllib.request.urlopen(request, timeout=20):
            pass

    def _authorization(
        self,
        method: str,
        canonical_uri: str,
        headers: dict[str, str],
        payload_hash: str,
        amz_date: str,
        date_stamp: str,
    ) -> str:
        signed_header_names = sorted(name.lower() for name in headers)
        canonical_headers = "".join(
            f"{name.lower()}:{headers[name].strip()}\n"
            for name in sorted(headers, key=str.lower)
        )
        credential_scope = f"{date_stamp}/{self.region}/s3/aws4_request"
        canonical_request = "\n".join(
            [
                method,
                canonical_uri,
                "",
                canonical_headers,
                ";".join(signed_header_names),
                payload_hash,
            ],
        )
        string_to_sign = "\n".join(
            [
                "AWS4-HMAC-SHA256",
                amz_date,
                credential_scope,
                hashlib.sha256(canonical_request.encode()).hexdigest(),
            ],
        )
        signing_key = self._signing_key(date_stamp)
        signature = hmac.new(
            signing_key,
            string_to_sign.encode(),
            hashlib.sha256,
        ).hexdigest()
        return (
            "AWS4-HMAC-SHA256 "
            f"Credential={self.access_key_id}/{credential_scope}, "
            f"SignedHeaders={';'.join(signed_header_names)}, "
            f"Signature={signature}"
        )

    def _signing_key(self, date_stamp: str) -> bytes:
        assert self.secret_access_key is not None
        date_key = _sign(f"AWS4{self.secret_access_key}".encode(), date_stamp)
        date_region_key = _sign(date_key, self.region)
        date_region_service_key = _sign(date_region_key, "s3")
        return _sign(date_region_service_key, "aws4_request")

    def _public_url(self, key: str) -> str:
        assert self.bucket is not None
        encoded_key = "/".join(urllib.parse.quote(part) for part in key.split("/"))
        return f"https://{self.bucket}.s3.{self.region}.amazonaws.com/{encoded_key}"


def _sign(key: bytes, message: str) -> bytes:
    return hmac.new(key, message.encode(), hashlib.sha256).digest()
