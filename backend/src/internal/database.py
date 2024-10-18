from sqlmodel import Field, SQLModel, select
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker

__all__ = ("User", "get_user_by_email", "get_user_by_uuid", "get_session", "init_db")

# TODO: migrations


class User(SQLModel, table=True):
    uuid: str = Field(primary_key=True, index=True)
    email: str = Field(index=True, unique=True)
    password: str = Field(index=True)
    name: str = Field(index=True)
    surname: str = Field(index=True)
    middle_name: str = Field(index=True)


DATABASE_URL = "postgresql+asyncpg://inpad:tuyweytghgb@localhost/inpad_db"

# async engine
engine = create_async_engine(DATABASE_URL)

AsyncSessionLocal = sessionmaker(
    bind=engine,
    class_=AsyncSession,
    expire_on_commit=False,
    autoflush=False,
    autocommit=False,
)


async def init_db():
    async with engine.begin() as conn:
        await conn.run_sync(SQLModel.metadata.create_all)


async def get_session() -> AsyncSession:
    async with AsyncSessionLocal() as session:
        async with session.begin():
            return session


async def get_user_by_email(email: str) -> User | None:
    async with AsyncSessionLocal() as session:
        async with session.begin():
            statement = select(User).where(User.email == email)
            result = await session.execute(statement)
            user = result.scalars().first()
            return user


async def get_user_by_uuid(uuid: str) -> User | None:
    async with AsyncSessionLocal() as session:
        async with session.begin():
            statement = select(User).where(User.uuid == uuid)
            result = await session.execute(statement)
            user = result.scalars().first()
            return user
