from sqlalchemy import create_engine, Column, Integer, String, Boolean, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship, sessionmaker

engine = create_engine("sqlite:///my_database.db", echo=True)
Base = declarative_base()

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

# Создание таблиц
Base.metadata.create_all(engine)
