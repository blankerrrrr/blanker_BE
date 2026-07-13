from sqlalchemy.ext.asyncio import async_sessionmaker, create_async_engine

from app.core.config import settings

# DB와의 실제 연결을 관리하는 객체
# create_async_engine: 비동기(async) 버전 엔진 생성
# pool_pre_ping=True: 커넥션이 죽었을 경우 새로운 커넥션으로 교체
engine = create_async_engine(settings.database_url, pool_pre_ping=True)

# 세션 팩토리 생성
# SQLAlchemy는 기본적으로 commit하면 세션이 들고 있던 객체들을 만료(expire) 처리함
# expire_on_commit: commit 후에도 객체가 값을 그대로 들고 있어서 재조회 없이 사용 가능
async_session = async_sessionmaker(engine, expire_on_commit=False)
