import random
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine
from settings import PATH
from create_tables import Users, Words, Experience, Victory


class Connectbase:
    def __init__(self, PATH, user_name=None,
                 user_id=None,
                 new_rus_word=None,
                 new_eng_word=None):
        self.PATH = PATH
        self.user_name = user_name
        self.user_id = user_id
        self.new_rus_word = new_rus_word
        self.new_eng_word = new_eng_word

    def createuser(self):
        """Создание юзера в базе"""
        engine = create_engine(self.PATH)
        with sessionmaker(bind=engine)() as session:
            session.add(Users(user_name=self.user_name,
                              user_id=self.user_id))
            session.commit()

    def check_user(self):
        """проверка наличия пользователя в базе"""
        engine = create_engine(self.PATH)
        with sessionmaker(bind=engine)() as session:
            query = session.query(Users.user_id)
            result = query.filter(Users.user_id == self.user_id).all()
            return result

    def random_word(self):
        engine = create_engine(self.PATH)
        with sessionmaker(bind=engine)() as session:
            subq = session.query(Users.id).filter(Users.user_id == self.user_id).scalar_subquery()
            query = session.query(Words.rus_word, Words.eng_word).filter(
                (Words.word_user == subq) | (Words.word_user == None)
            ).all()
            random_words = random.sample(query, min(4, len(query)))
            return random_words

    def add_word(self):
        try:
            engine = create_engine(self.PATH)
            with sessionmaker(bind=engine)() as session:
                query = session.query(Users.id)
                result = query.filter(Users.user_id == self.user_id).all()[0][0]
                new_word = Words(
                    eng_word=self.new_eng_word,
                    rus_word=self.new_rus_word,
                    word_user=result)
                session.add(new_word)
                session.commit()
                result_add = 0
                return result_add
        except:
            result_add = 1
            return result_add

    def del_word(self):
        try:
            engine = create_engine(self.PATH)
            with sessionmaker(bind=engine)() as session:
                subq = session.query(Users.id).filter(Users.user_id == self.user_id).scalar()
                query_to_delete = session.query(Words).filter(Words.word_user == subq,
                                                              Words.rus_word == self.new_rus_word).first()
                session.delete(query_to_delete)
                session.commit()
                result = f'Удалено из базы слово : {self.new_rus_word}'
                return result
        except:
            result = f'Вы ещё не добавиляли слово {self.new_rus_word}'
            return result

    def check_word(self):
        engine = create_engine(self.PATH)
        with sessionmaker(bind=engine)() as session:
            subq = session.query(Users.id).filter(Users.user_id == self.user_id).scalar()
            query = session.query(Words).filter(Words.word_user == subq,
                                                Words.rus_word == self.new_rus_word).count()
            return query

    def my_word(self):
        engine = create_engine(self.PATH)
        with sessionmaker(bind=engine)() as session:
            subq = session.query(Users.id).filter(Users.user_id == self.user_id)
            query = session.query(Words.rus_word).filter(Words.word_user == subq[0][0]).all()
            result = []
            for my_word_information in query:
                result.append(my_word_information[0])
            if not result:
                result = "Вы не добавили слов"
                return result
            else:
                return result

    def experience_user(self):
        engine = create_engine(self.PATH)
        with sessionmaker(bind=engine)() as session:
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

    def get_experience_user(self):
        """Получение информации об успешных сопоставлениях"""
        engine = create_engine(self.PATH)
        with sessionmaker(bind=engine)() as session:
            query = (
                session.query(Experience)
                .join(Users, Users.id == Experience.user_exp)
                .filter(Users.user_id == self.user_id)
                .count()
            )
            return query

    def victory_word(self):
        engine = create_engine(self.PATH)
        with sessionmaker(bind=engine)() as session:
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

    def check_victory_word(self):
        engine = create_engine(self.PATH)
        with sessionmaker(bind=engine)() as session:
            query = session.query(Victory.eng_word).filter(Victory.id == self.user_id).first()
            return query


def registration(user_name, user_id):
    """регистрация пользователя"""
    Connectbase(PATH, user_name, str(user_id)).createuser()


def check_registration(user_id):
    """проверка регистрации"""
    result = Connectbase(PATH, None, str(user_id)).check_user()
    if not result:
        return None
    else:
        return result[0]


def get_random_word(user_id):
    """получить 4 случайных пары слов"""
    result = Connectbase(PATH, None, str(user_id)).random_word()
    return result


def add_word_db(id_user_word, new_rus_word, new_eng_word):
    """Добавить слово"""
    result = Connectbase(PATH, None, str(id_user_word), new_rus_word, new_eng_word).add_word()
    return result


def del_word_db(user_id, new_rus_word):
    """Удаление слова"""
    result = Connectbase(PATH, None, str(user_id), new_rus_word).del_word()
    return result


def get_my_word(user_id):
    """Получить список моих слов"""
    result = Connectbase(PATH, None, str(user_id)).my_word()
    return result


def add_experience(id_user_word, new_eng_word):
    """Добавить изученное слово"""
    result = Connectbase(PATH, None, str(id_user_word), None, new_eng_word).experience_user()
    return result


def get_experience(id_user_word):
    """Добавить изученное слово"""
    result = Connectbase(PATH, None, str(id_user_word), None, None).get_experience_user()
    return result


def get_check_word(id_user_word, new_rus_word):
    result = Connectbase(PATH, None, str(id_user_word), new_rus_word, None).check_word()
    return result


def add_victory(id_user, rus_word, eng_word):
    """Запись связки перевода для юзера"""
    Connectbase(PATH, None, str(id_user), rus_word, eng_word).victory_word()


def check_victory(id_user_word):
    """проверка связки перевода для юзера"""
    result = Connectbase(PATH, None, str(id_user_word), None, None).check_victory_word()
    return result
