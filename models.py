from sqlalchemy import Column, Integer, String, Boolean, ForeignKey, DateTime, Index, UniqueConstraint
from sqlalchemy.orm import relationship, DeclarativeBase
from enum import Enum
from sqlalchemy import Enum as SQLEnum
from datetime import datetime, timezone


class PaymentType(str, Enum):
    INCOGNITO = "incognito"
    COLLECTION = "collection"


class Gender(str, Enum):
    MAN = "MAN"
    WOMAN = "WOMAN"
    ANY = "ANY"


# Новый стиль декларативной базы для современного SQLAlchemy
class Base(DeclarativeBase):
    pass


# Таблица users
class User(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True, autoincrement=True)
    telegram_id = Column(Integer, unique=True, nullable=False)
    first_name = Column(String)
    username = Column(String)
    gender = Column(SQLEnum(Gender, name="gender_enum", native_enum=False), nullable=True)
    gender_search = Column(SQLEnum(Gender, name="gender_search_enum", native_enum=False), nullable=True)
    country = Column(String)
    country_local = Column(String)
    city = Column(String)
    city_local = Column(String)
    photo_id = Column(String)
    about_me = Column(String)
    eighteen_years_and_approval = Column(Boolean)
    incognito_pay = Column(Boolean, default=False, nullable=False)
    incognito_switch = Column(Boolean, default=False, nullable=False)
    banned = Column(Boolean, default=False, nullable=False)

    # Обратные связи
    reactions_sent = relationship('Reaction', foreign_keys='Reaction.telegram_id', back_populates='sender')
    reactions_received = relationship('Reaction', foreign_keys='Reaction.target_tg_id', back_populates='receiver')
    payments_made = relationship('Payment', foreign_keys='Payment.telegram_id', back_populates='buyer')
    payments_received = relationship('Payment', foreign_keys='Payment.target_tg_id', back_populates='target')
    caches = relationship('Cache', foreign_keys='Cache.telegram_id', back_populates='user')


# Таблица reactions
class Reaction(Base):
    __tablename__ = 'reactions'

    id = Column(Integer, primary_key=True, autoincrement=True)
    telegram_id = Column(Integer, ForeignKey('users.telegram_id'), nullable=False)
    target_tg_id = Column(Integer, ForeignKey('users.telegram_id'), nullable=False)
    reaction = Column(String)

    sender = relationship('User', foreign_keys=[telegram_id], back_populates='reactions_sent')
    receiver = relationship('User', foreign_keys=[target_tg_id], back_populates='reactions_received')

    __table_args__ = (
        Index('ix_reactions_telegram_target_reaction', telegram_id, target_tg_id, reaction),
        Index('ix_reactions_target_tg_id', target_tg_id),
        UniqueConstraint('telegram_id', 'target_tg_id', name='uq_reaction_pair'),
    )


# Таблица payment
class Payment(Base):
    __tablename__ = 'payments'

    id = Column(Integer, primary_key=True, autoincrement=True)
    telegram_id = Column(Integer, ForeignKey('users.telegram_id'), nullable=False)
    target_tg_id = Column(Integer, ForeignKey('users.telegram_id'), nullable=True)
    amount = Column(Integer, nullable=False)
    type = Column(SQLEnum(PaymentType, name="payment_type_enum", native_enum=False), nullable=False)
    created_at = Column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))

    buyer = relationship('User', foreign_keys=[telegram_id], back_populates='payments_made')
    target = relationship('User', foreign_keys=[target_tg_id], back_populates='payments_received')



# Таблица кэш
class Cache(Base):
    __tablename__ = 'cache'

    id = Column(Integer, primary_key=True, autoincrement=True)
    telegram_id = Column(Integer, ForeignKey('users.telegram_id'), nullable=False)
    parameter = Column(String)
    message_id = Column(Integer)

    user = relationship('User', foreign_keys=[telegram_id], back_populates='caches')


# Примечание: создание таблиц теперь происходит в основном коде через async engine


# виды реакций
class ReactionType(str, Enum):
    LOVE = "LOVE"
    SEX = "SEX"
    CHAT = "CHAT"
    SKIP = "SKIP"
