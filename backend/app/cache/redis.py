from redis.asyncio import Redis

from app.core.config import settings


# decode_responses=True: 바이트 문자열을 UTF-8로 자동 변환
# protocol=2: Redis 통신 프로토콜(RESP) 버전 2 (RESP2) 지정
def create_redis_client() -> Redis:
    return Redis.from_url(settings.redis_url, decode_responses=True, protocol=2)
