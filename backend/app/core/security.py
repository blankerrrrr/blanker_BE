import hashlib
import hmac
import secrets
from datetime import UTC, datetime, timedelta

from argon2 import PasswordHasher
from argon2 import exceptions as argon2_exceptions
from jose import JWTError, jwt

from app.core.config import settings

password_hasher = PasswordHasher()


def hash_password(password: str) -> str:
    return password_hasher.hash(password)


def verify_password(password: str, password_hash: str) -> bool:
    if password_hash.startswith("pbkdf2_sha256$"):
        return _verify_pbkdf2_password(password, password_hash)

    try:
        return password_hasher.verify(password_hash, password)
    except (
        argon2_exceptions.InvalidHashError,
        argon2_exceptions.VerificationError,
        argon2_exceptions.VerifyMismatchError,
    ):
        return False


def _verify_pbkdf2_password(password: str, password_hash: str) -> bool:
    try:
        algorithm, salt, expected_digest = password_hash.split("$", 2)
    except ValueError:
        return False

    if algorithm != "pbkdf2_sha256":
        return False

    actual_digest = hashlib.pbkdf2_hmac(
        "sha256",
        password.encode("utf-8"),
        salt.encode("utf-8"),
        120_000,
    ).hex()
    return hmac.compare_digest(actual_digest, expected_digest)


def hash_token(token: str) -> str:
    return hashlib.sha256(token.encode("utf-8")).hexdigest()


def create_access_token(user_id: str) -> tuple[str, int]:
    expires_delta = timedelta(minutes=settings.access_token_expires_minutes)
    expires_at = datetime.now(UTC) + expires_delta
    payload = {
        "sub": user_id,
        "type": "access",
        "exp": expires_at,
        "iat": datetime.now(UTC),
    }
    token = jwt.encode(
        payload,
        settings.jwt_secret_key,
        algorithm=settings.jwt_algorithm,
    )
    return token, int(expires_delta.total_seconds())


def decode_access_token(token: str) -> str | None:
    try:
        payload = jwt.decode(
            token,
            settings.jwt_secret_key,
            algorithms=[settings.jwt_algorithm],
        )
    except JWTError:
        return None

    if payload.get("type") != "access":
        return None

    subject = payload.get("sub")
    return subject if isinstance(subject, str) else None


def create_refresh_token(user_id: str) -> tuple[str, str]:
    token_id = secrets.token_hex(16)
    raw_token = secrets.token_urlsafe(48)
    return f"{user_id}.{token_id}.{raw_token}", token_id


def parse_refresh_token(token: str) -> tuple[str, str] | None:
    parts = token.split(".", 2)
    if len(parts) != 3:
        return None
    user_id, token_id, raw_token = parts
    if not user_id or not token_id or not raw_token:
        return None
    return user_id, token_id
