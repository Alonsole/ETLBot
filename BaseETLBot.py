import sqlalchemy
import sqlalchemy as sq
import json
import random
from sqlalchemy.orm import sessionmaker, relationship
from sqlalchemy.orm import declarative_base
from sqlalchemy import func

Base = declarative_base()


class Connectbase:
    def __init__(self, name, passw, server, port, name_db, sqlm, user_name=None, user_id=None,
                 new_rus_word=None, new_eng_word=None):
        self.name = name
        self.passw = passw
        self.server = server
        self.port = port
        self.database = name_db
        self.sqlm = sqlm
        self.user_name = user_name
        self.user_id = user_id
        self.new_rus_word = new_rus_word
        self.new_eng_word = new_eng_word
        self.DSN = f"{self.sqlm}://{self.name}:{self.passw}@{self.server}:{self.port}/{self.database}"

    def creatdb(self):
        """Создание базы"""
        engine = sqlalchemy.create_engine(self.DSN)
        Base.metadata.create_all(engine)
        Session = sessionmaker(bind=engine)
        session = Session()
        session.close()
        return print("Создана база из 3х таблиц")

    def createuser(self):
        """Создание юзера в базе"""
        engine = sqlalchemy.create_engine(self.DSN)
        Session = sessionmaker(bind=engine)
        session = Session()
        session.add(Users(user_name=self.user_name,
                          user_id=self.user_id))
        session.commit()
        session.close()

    def check_user(self):
        """проверка наличия пользователя в базе"""
        engine = sqlalchemy.create_engine(self.DSN)
        Session = sessionmaker(bind=engine)
        session = Session()
        query = session.query(Users.user_id)
        result = query.filter(Users.user_id == self.user_id).all()
        session.close()
        return result

    def loaddataword(self):
        """Загрузка тестовой базы"""
        engine = sqlalchemy.create_engine(self.DSN)
        Session = sessionmaker(bind=engine)
        session = Session()
        for record in data:
            new_word = Words(
                id=record.get('id'),
                eng_word=record.get('word_eng'),
                rus_word=record.get('word_rus').encode('cp1251').decode('utf-8'))
            session.add(new_word)
        session.commit()
        session.close()
        return print("Загружена тестовая база слов")

    def random_word(self):
        engine = sqlalchemy.create_engine(self.DSN)
        Session = sessionmaker(bind=engine)
        session = Session()
        subq = session.query(Users.id).filter(Users.user_id == self.user_id).scalar_subquery()
        query = session.query(Words.rus_word, Words.eng_word).filter(
            (Words.word_user == subq) | (Words.word_user == None)
        ).all()
        random_words = random.sample(query, min(4, len(query)))
        session.close()
        return random_words

    def add_word(self):
        try:
            engine = sqlalchemy.create_engine(self.DSN)
            Session = sessionmaker(bind=engine)
            session = Session()
            query = session.query(Users.id)
            result = query.filter(Users.user_id == self.user_id).all()[0][0]
            word_count = session.query(func.max(Words.id)).scalar()
            new_word = Words(
                id=word_count + 1,
                eng_word=self.new_eng_word,
                rus_word=self.new_rus_word,
                word_user=result)
            session.add(new_word)
            session.commit()
            session.close()
            result_add = 0
            return result_add
        except:
            result_add = 1
            return result_add

    def del_word(self):
        try:
            engine = sqlalchemy.create_engine(self.DSN)
            Session = sessionmaker(bind=engine)
            session = Session()
            subq = session.query(Users.id).filter(Users.user_id == self.user_id).scalar()
            query_to_delete = session.query(Words).filter(Words.word_user == subq,
                                                          Words.rus_word == self.new_rus_word).first()
            session.delete(query_to_delete)
            session.commit()
            session.close()
            result = f'Удалено из базы слово : {self.new_rus_word}'
            return result
        except:
            result = f'Вы ещё не добавиляли слово {self.new_rus_word}'
            return result

    def check_word(self):

        engine = sqlalchemy.create_engine(self.DSN)
        Session = sessionmaker(bind=engine)
        session = Session()
        subq = session.query(Users.id).filter(Users.user_id == self.user_id).scalar()
        query = session.query(Words).filter(Words.word_user == subq,
                                            Words.rus_word == self.new_rus_word).count()
        session.close()
        return query

    def my_word(self):
        engine = sqlalchemy.create_engine(self.DSN)
        Session = sessionmaker(bind=engine)
        session = Session()
        subq = session.query(Users.id).filter(Users.user_id == self.user_id)
        query = session.query(Words.rus_word).filter(Words.word_user == subq[0][0]).all()
        result = []
        for my_word_information in query:
            result.append(my_word_information[0])
        session.close()
        if not result:
            result = "Вы не добавили слов"
            return result
        else:
            return result

    def experience_user(self):
        engine = sqlalchemy.create_engine(self.DSN)
        Session = sessionmaker(bind=engine)
        session = Session()
        query = session.query(Users.id)
        result = query.filter(Users.user_id == self.user_id).all()[0][0]
        # Проверяем, существует ли уже слово для данного пользователя
        existing_word = session.query(Experience).filter_by(user_exp=result, eng_word_exp=self.new_eng_word).first()
        if existing_word is None:
            # Если слово не существует, добавляем его в базу данных
            word_exp = Experience(
                eng_word_exp=self.new_eng_word,
                user_exp=result
            )
            session.add(word_exp)
            session.commit()
        else:
            pass

        session.close()

    def get_experience_user(self):
        engine = sqlalchemy.create_engine(self.DSN)
        Session = sessionmaker(bind=engine)
        session = Session()
        subq = session.query(Users.id).filter(Users.user_id == self.user_id)
        query = session.query(Experience).filter(Experience.user_exp == subq[0][0]).count()
        session.close()
        return query

    def victory_word(self):
        engine = sqlalchemy.create_engine(self.DSN)
        Session = sessionmaker(bind=engine)
        session = Session()
        query = session.query(Victory).filter(Victory.id == self.user_id).first()
        if query is not None:
            session.delete(query)
            session.commit()
        victory_word = Victory(
            id=self.user_id,
            eng_word=self.new_eng_word,
            rus_word=self.new_rus_word)
        session.add(victory_word)
        session.commit()
        session.close()

    def check_victory_word(self):
        engine = sqlalchemy.create_engine(self.DSN)
        Session = sessionmaker(bind=engine)
        session = Session()
        query = session.query(Victory.eng_word).filter(Victory.id == self.user_id).first()
        session.close()
        return query

with open('dataword.json', 'r') as f:
    data = json.load(f)


class Users(Base):
    __tablename__ = "users"
    id = sq.Column(sq.Integer, primary_key=True)
    user_name = sq.Column(sq.String(length=250), unique=True)
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


"""подключается к БД любого типа на ваш выбор"""
name = "postgres"
passw = 'Пароль'
server = "localhost"
port = "Порт"
name_db = "Указать базу"
sqlm = "postgresql"


def createdatabase():
    """создание базы"""
    result = Connectbase(name, passw, server, port, name_db, sqlm).creatdb()
    return result


def loadworddatabase():
    """заливка базы"""
    result = Connectbase(name, passw, server, port, name_db, sqlm).loaddataword()
    return result


def registration(user_name, user_id):
    """регистрация пользователя"""
    Connectbase(name, passw, server, port, name_db, sqlm, user_name,
                str(user_id)).createuser()


def check_registration(user_id):
    """проверка регистрации"""
    result = Connectbase(name, passw, server, port, name_db, sqlm, None,
                         str(user_id)).check_user()
    if not result:
        return None
    else:
        return result[0]


def get_random_word(user_id):
    """получить 4 случайных пары слов"""
    result = Connectbase(name, passw, server, port, name_db, sqlm, None,
                         str(user_id)).random_word()
    return result


def add_word_db(id_user_word, new_rus_word, new_eng_word):
    """Добавить слово"""
    result = Connectbase(name, passw, server, port, name_db, sqlm, None,
                         str(id_user_word), new_rus_word, new_eng_word).add_word()
    return result


def del_word_db(user_id, new_rus_word):
    """Удаление слова"""
    result = Connectbase(name, passw, server, port, name_db, sqlm, None,
                         str(user_id), new_rus_word).del_word()
    return result


def get_my_word(user_id):
    """Получить список моих слов"""
    result = Connectbase(name, passw, server, port, name_db, sqlm, None,
                         str(user_id)).my_word()
    return result


def add_experience(id_user_word, new_eng_word):
    """Добавить изученное слово"""
    result = Connectbase(name, passw, server, port, name_db, sqlm, None,
                         str(id_user_word), None, new_eng_word).experience_user()
    return result


def get_experience(id_user_word):
    """Добавить изученное слово"""
    result = Connectbase(name, passw, server, port, name_db, sqlm, None,
                         str(id_user_word), None, None).get_experience_user()
    return result


def get_check_word(id_user_word, new_rus_word):
    result = Connectbase(name, passw, server, port, name_db, sqlm, None,
                         str(id_user_word), new_rus_word, None).check_word()
    return result


def add_victory(id_user, rus_word, eng_word):
    """Запись связки перевода для юзера"""
    Connectbase(name, passw, server, port, name_db, sqlm, None,
                         str(id_user), rus_word, eng_word).victory_word()


def check_victory(id_user_word):
    """проверка связки перевода для юзера"""
    result = Connectbase(name, passw, server, port, name_db, sqlm, None,
                         str(id_user_word), None, None).check_victory_word()
    return result


