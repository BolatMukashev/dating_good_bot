from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker
from config import DATABASE_URL

async_engine = create_async_engine(DATABASE_URL, echo=False)

AsyncSessionLocal = async_sessionmaker(
    bind=async_engine,
    expire_on_commit=False
)


# import ssl
# from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker
# from config import DATABASE_URL

# # Создаём SSL-контекст
# ssl_context = ssl.create_default_context()
# ssl_context.check_hostname = False
# ssl_context.verify_mode = ssl.CERT_NONE  # если не хочешь проверять сертификат

# # В движок передаём connect_args
# async_engine = create_async_engine(
#     DATABASE_URL,
#     echo=False,
#     connect_args={"ssl": ssl_context}
# )

# AsyncSessionLocal = async_sessionmaker(
#     bind=async_engine,
#     expire_on_commit=False
# )
