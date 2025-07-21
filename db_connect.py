from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker
from config import DATABASE_URL

async_engine = create_async_engine(DATABASE_URL, echo=False)

AsyncSessionLocal = async_sessionmaker(
    bind=async_engine,
    expire_on_commit=False
)
