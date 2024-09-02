# Документация - Описание функций

### Документация будет обновлена!!!!

## 1. Скрипты:
1. ETLBot.py - отвечает за работу визуальной части Телеграм бота. Запрашивает информацию из BaseETLBot.py.
2. BaseETLBot.py - функции работы с базой SQL
## 2. Файлы:
1. requirements.txt - это простой текстовый файл, который содержит перечень всех модулей и пакетов, необходимых для корректной работы программы.
2. dataword.json - тестовая база слов. Объем 30 слов.

## Описание содержания скриптов.
ETLBot.py
- class Addword - используется для добавления новых слов.
- class Command - все кнопки бота в одном месте.
- def send_welcome(message) - функция отвечает за первый старт программы, приветсвие, отображение дальнейших действий по регистрации или запуску. 
- def help_message(message) - бот присылает краткую информацию о своих возможностях
- def registartion(message) - запись в базу нового пользователя. 
- def start_of_studies(message) - начала обучения. Загружается первое случайное слово и 4 варианта ответа. 
- def add_word(message) - запрос добавления слова с последующим вызовом функции send_add_word(message).
- def send_add_word(message) - отправка нового слова и его перевода в базу
- def send_cancel_word(message) - возврат к функции start_of_studies(message).
- def my_word_list(message): - вывод информации о добавленных Вами словах
- def my_experience(message) - количество верных ответов.
- def del_word(message) - удаление добавленного Вами слова
- def next_word(message) - возврат к функции start_of_studies(message).
- def message_reply(message) - ответ бота на верное сопоставление или ошибочный ответ.
  
BaseETLBot.py
- class Connectbase: - единый вход для работы с базой.
- def creatdb(self) - функция создания базы.
- def createuser(self) - создание пользователей.
- def check_user(self) - проверка регистрации пользователя.
- def loaddataword(self) - загрузка базы слов (знаний)
- def random_word(self) - загружает и возврашщает 4 слова для сопоставления.
- def add_word(self) - добавление слова в базу.
- def del_word(self) - удаление слова из базы.
- check_word(self) - проверка наличия слова в базе.
- def my_word(self) - вывод списка добавленных слов.
- def experience_user(self) - запись верных сопоставлений.
- def get_experience_user(self) - запрос и отображение информации о количестве верных сопоставлений.
- def victory_word(self) - хранение верной связи слов для каждого пользователя.
- def check_victory_word(self) - проверка верной связи и отправка боту.
  
Создание базы (BaseETLBot.py):
- class Users(Base) - данные пользователей.
- class Words(Base) - список слов.
- class Experience(Base) - опыт пользователя.
- class Victory(Base) - связка верных сопоставлений для пользователей.

Настройки подключения к базе (BaseETLBot.py):
- name = "postgres"
- passw = 'Ваш пароль подключения к базе'
- server = "localhost"
- port = "№ порта"
- name_db = "Название базы"
- sqlm = "postgresql"

Запуск функций (BaseETLBot.py):
- def createdatabase() - создание базы
- def loadworddatabase() - заливка базы
- def registration(user_name, user_id) - регистрация пользователя
- def check_registration(user_id) - проверка регистрации
- def get_random_word(user_id) - получить 4 случайных пары слов
- def add_word_db(id_user_word, new_rus_word, new_eng_word) - Добавить слово
- def del_word_db(user_id, new_rus_word) - Удаление слова
- def get_my_word(user_id) - Получить список моих слов
- def add_experience(id_user_word, new_eng_word) - Добавить изученное слово
- def get_experience(id_user_word) - Добавить изученное слово
- def get_check_word(id_user_word, new_rus_word) - Проверка слова
- def add_victory(id_user, rus_word, eng_word) - Запись связки перевода для юзера
- def check_victory(id_user_word) - проверка связки перевода для юзера
