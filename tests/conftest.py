import asyncio
import pytest
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker

from bot.db.base import Base
import bot.db.sessions as db_sessions


DATABASE_URL = "sqlite+aiosqlite:///:memory:"


@pytest.fixture(scope="session")
def event_loop():
    loop = asyncio.new_event_loop()
    yield loop
    loop.close()


@pytest.fixture(scope="session")
async def engine():
    engine = create_async_engine(DATABASE_URL)

    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

    yield engine
    await engine.dispose()


@pytest.fixture
async def session(engine):
    SessionMaker = async_sessionmaker(
        bind=engine,
        expire_on_commit=False,
    )

    async with SessionMaker() as session:
        yield session


@pytest.fixture(autouse=True)
def override_db(session, engine, monkeypatch):
    """
    КЛЮЧЕВОЕ МЕСТО
    """

    # 1️⃣ подменяем engine
    monkeypatch.setattr(db_sessions, "engine", engine)

    # 2️⃣ подменяем sessionmaker
    monkeypatch.setattr(
        db_sessions,
        "AsyncSessionLocal",
        async_sessionmaker(
            bind=engine,
            expire_on_commit=False,
        ),
    )

    # 3️⃣ подменяем get_session
    async def _get_session_override():
        yield session

    monkeypatch.setattr(db_sessions, "get_session", _get_session_override)
