import json
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from create_tables import Words


def load_data_word(PATH):
    """Загрузка тестовой базы"""
    engine = create_engine(PATH)
    with sessionmaker(bind=engine)() as session:
        for record in data:
            new_word = Words(
                eng_word=record.get('word_eng'),
                rus_word=record.get('word_rus').encode('cp1251').decode('utf-8'))
            session.add(new_word)
        session.commit()
    return print("Загружена тестовая база слов")


with open('dataword.json', 'r') as f:
    data = json.load(f)
