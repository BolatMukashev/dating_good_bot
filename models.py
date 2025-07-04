from sqlalchemy import Column, Integer, String, Boolean, ForeignKey, Text
from sqlalchemy.orm import relationship, DeclarativeBase
from enum import Enum


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
    gender = Column(String)
    gender_search = Column(String)
    country = Column(String)
    city = Column(String)
    about_me = Column(String)
    photo_id = Column(String)
    eighteen_years_old = Column(Boolean)

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


# Таблица payment
class Payment(Base):
    __tablename__ = 'payments'

    id = Column(Integer, primary_key=True, autoincrement=True)
    telegram_id = Column(Integer, ForeignKey('users.telegram_id'), nullable=False)
    target_tg_id = Column(Integer, ForeignKey('users.telegram_id'), nullable=False)
    price = Column(Integer)

    buyer = relationship('User', foreign_keys=[telegram_id], back_populates='payments_made')
    target = relationship('User', foreign_keys=[target_tg_id], back_populates='payments_received')


# Таблица кэш
class Cache(Base):
    __tablename__ = 'cache'

    id = Column(Integer, primary_key=True, autoincrement=True)
    telegram_id = Column(Integer, ForeignKey('users.telegram_id'), nullable=False)
    parameter = Column(String)
    message_id = Column(Integer)
    data = Column(Text)

    user = relationship('User', foreign_keys=[telegram_id], back_populates='caches')


# Примечание: создание таблиц теперь происходит в основном коде через async engine


# виды реакций
class ReactionType(str, Enum):
    LOVE = "LOVE"
    SEX = "SEX"
    CHAT = "CHAT"
    SKIP = "SKIP"

    @property
    def label(self):
        return {
            self.LOVE: "Свидание",
            self.SEX: "Постель",
            self.CHAT: "Общение",
            self.SKIP: "Пропуск",
        }[self]

    @property
    def message_template(self):
        return {
            self.LOVE: "Ты лайкнул {name}",
            self.SEX: "Ты лайкнул {name}",
            self.CHAT: "Ты лайкнул {name}",
            self.SKIP: "Ты пропустил {name}",
        }[self]
    

gender = {"MAN": "Мужчина", "WOMAN": "Женщина", "ANY": "Другое"}
gender_search = {"search_man": "Ищу Мужчину", "search_woman": "Ищу Женщину", "search_any": "Пол не имеет значения"}
gender_search_db = {"search_man": "MAN", "search_woman": "WOMAN", "search_any": "ANY"}