from create_db import create_object_db
from create_tables import create_tables
from word_base import load_data_word
from settings import PATH

if __name__ == '__main__':
    """Настройка Бота
    1. Создание ДатаБазы в PostgresSql - etlbase
    2. Заливка Таблиц в ДатаБазу
    """
    create_object_db(PATH)
    create_tables(PATH)
    load_data_word(PATH)
    print("Установка выполненна успешно")