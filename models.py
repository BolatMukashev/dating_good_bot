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
    eighteen_years_old = Column(Boolean)
    gender = Column(String)
    gender_search = Column(String)
    photo_id = Column(String)
    about_me = Column(String)
    country = Column(String)
    city = Column(String)

    # Обратные связи (необязательные, но удобные)
    reactions_sent = relationship('Reaction', foreign_keys='Reaction.telegram_id', back_populates='sender')
    reactions_received = relationship('Reaction', foreign_keys='Reaction.target_tg_id', back_populates='receiver')
    buys_made = relationship('Buy', foreign_keys='Buy.telegram_id', back_populates='buyer')
    buys_received = relationship('Buy', foreign_keys='Buy.target_tg_id', back_populates='target')

# Таблица reactions
class Reaction(Base):
    __tablename__ = 'reactions'

    id = Column(Integer, primary_key=True, autoincrement=True)
    telegram_id = Column(Integer, ForeignKey('users.telegram_id'), nullable=False)
    target_tg_id = Column(Integer, ForeignKey('users.telegram_id'), nullable=False)
    reaction = Column(String)

    sender = relationship('User', foreign_keys=[telegram_id], back_populates='reactions_sent')
    receiver = relationship('User', foreign_keys=[target_tg_id], back_populates='reactions_received')

# Таблица buy
class Buy(Base):
    __tablename__ = 'buy'

    id = Column(Integer, primary_key=True, autoincrement=True)
    telegram_id = Column(Integer, ForeignKey('users.telegram_id'), nullable=False)
    target_tg_id = Column(Integer, ForeignKey('users.telegram_id'), nullable=False)
    price = Column(Integer)

    buyer = relationship('User', foreign_keys=[telegram_id], back_populates='buys_made')
    target = relationship('User', foreign_keys=[target_tg_id], back_populates='buys_received')

# Создание таблиц
Base.metadata.create_all(engine)
