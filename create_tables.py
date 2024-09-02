import sqlalchemy as sq
from sqlalchemy import create_engine
from sqlalchemy.orm import relationship, sessionmaker
from settings import Base


class Users(Base):
    __tablename__ = "users"
    id = sq.Column(sq.Integer, primary_key=True)
    user_name = sq.Column(sq.String(length=250), unique=False)
    user_id = sq.Column(sq.String(length=20), unique=True)


class Words(Base):
    __tablename__ = "words"
    id = sq.Column(sq.Integer, primary_key=True, autoincrement=True)
    eng_word = sq.Column(sq.String(length=250), unique=False)
    rus_word = sq.Column(sq.String(length=250), unique=False)
    word_user = sq.Column(sq.Integer, sq.ForeignKey("users.id"))
    users = relationship("Users", backref="words")


class Experience(Base):
    __tablename__ = "experience"
    id = sq.Column(sq.Integer, primary_key=True, autoincrement=True)
    eng_word_exp = sq.Column(sq.String(length=250), unique=False)
    user_exp = sq.Column(sq.Integer, sq.ForeignKey("users.id"))
    users = relationship("Users", backref="experience")


class Victory(Base):
    __tablename__ = "victory"
    id = sq.Column(sq.String(length=250), primary_key=True)
    eng_word = sq.Column(sq.String(length=250), unique=False)
    rus_word = sq.Column(sq.String(length=250), unique=False)


def create_tables(PATH):
    engine = create_engine(PATH)
    with sessionmaker(bind=engine)() as session:
        Base.metadata.create_all(engine)
        session.commit()
        print('БД успешна создана')