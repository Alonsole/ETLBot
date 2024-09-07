import random
import re
from settings import bot
from telebot import types
import BaseETLBot


class Addword:
    id_user_word = None
    new_rus_word = None
    new_eng_word = None
    id_add_word = 0


class Command:
    """Все кнопки тут"""
    registation = types.KeyboardButton("Зарегистрироваться 🆗")
    next_word = types.KeyboardButton("Далее ⏩")
    add_word = types.KeyboardButton("Добавить слово ➕")
    my_word = types.KeyboardButton("Мои слова ✍")
    help_b = types.KeyboardButton("Помощь 💬")
    btn_start = types.KeyboardButton("Запуск 🆗")
    back = types.KeyboardButton("Назад ⏪")
    my_experience = types.KeyboardButton("Статистика обучения 🏆")


@bot.message_handler(commands=['start'])
def send_welcome(message):
    global user_info
    user_info = message.from_user.first_name
    """Приветствие"""
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    user_id = message.from_user.id  # передаю в базу ид пользователя
    check_registration = BaseETLBot.check_registration(user_id)  # запускаю проверку пользователя
    if check_registration is None:  # если пользователя нет = создаём
        btn_first = types.KeyboardButton(Command.registation.text)
    else:
        btn_first = types.KeyboardButton(Command.btn_start.text)
    markup.add(btn_first, Command.help_b)
    bot.reply_to(message, f"Здравствуйте, уважаемый {user_info} 👋 \n"
                          f"Бот создан с целью практических занятий английскому языку. \n"
                          "База содержит - 9954 слова🧡"
                          "Тренировки можете проходить в удобном для Вас темпе и в любое удобное вермя ⌚. \n"
                          "У Вас есть возможность добавлять личные слова, которые будут доступны только Вам.\n"
                          "Вы сможете собрать свою собственную базу для обучения 💎.  \n"
                          "Для продолжения используйте меню ⬇️", reply_markup=markup)


@bot.message_handler(func=lambda message: message.text == Command.help_b.text)
def help_message(message):
    """Всё просто это HELP"""
    bot.reply_to(message, f"Описание возможностей и функций кнопок 📑\n"
                          f"Первые четыре кнопки отображают варианты перевода слова, который Бот Вам "
                          f"предложил. Только один верный вариант 🎲. "
                          f"Не беспокойтесь, попытки неограничены 💪, а также Вы можете пропустить слово ⏩\n"
                          f"| {Command.next_word.text} | используйте для перехода к следующей странице слов.\n"
                          f"| {Command.add_word.text} | добавляет слово на 🇷🇺 и 🏴󠁧󠁢󠁥󠁮󠁧󠁿 языке"
                          "в вашу личную базу знаний.\n"
                          f"| {Command.my_word.text} | показать список добавленных Вами слов \n"
                          f"| {Command.my_experience.text} | вывод статистики успешных сопоставлений слов\n"
                          f"Внимание ‼ Добавляйте слова аккуратно и указывайте верный перевод \n"
                          f"Если Вы случайно создали ошибочное слово 🙁 - Удалите его ‼\n"
                          f"Добавленные слова доступны только пользователю добавившему слово 😜")


@bot.message_handler(func=lambda message: message.text == Command.registation.text)
def registartion(message):
    """Регистрация нового юзера для учёта слов"""
    user_id = message.from_user.id  # передаю в базу ид пользователя
    BaseETLBot.registration(user_info, user_id)
    bot.reply_to(message, f"Спасибо 🤝, {user_info} за регистрацию и внимание к данному Боту 🛸")
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    markup.add(Command.btn_start, Command.help_b)
    bot.send_message(message.chat.id, text=f"{user_info}. Для продолжения нажмите Запуск ⚡", reply_markup=markup)


@bot.message_handler(func=lambda message: message.text == Command.btn_start.text)
def start_of_studies(message):
    """Пользователь зарегистрировался и стартовал!"""
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    user_id = message.from_user.id
    random_word = BaseETLBot.get_random_word(user_id)
    rus_word = random_word[0][0]
    global eng_word
    eng_word = random_word[0][1]
    wrong_word_one = random_word[1][1]
    wrong_word_two = random_word[2][1]
    wrong_word_three = random_word[3][1]
    buttons = [eng_word, wrong_word_one, wrong_word_two, wrong_word_three]
    random.shuffle(buttons)
    markup.add(*buttons,
               Command.next_word,
               Command.add_word,
               Command.my_word,
               Command.my_experience,
               Command.help_b)
    message_question = ["Выберите верный перевод слова ?",
                        "Выберите правильный перевод слова ?",
                        "Какой из перечисленных вариантов перевода слова является правильным ?",
                        "Как правильно переводится слово ?",
                        "Вам нужно выбрать один вариант перевода слова:",
                        "Попробуйте угадать верный перевод слова:",
                        "Вы знаете верный перевод слова?,"
                        "Нажмите на кнопку с верным переводом слова."
                        "Угадаете перевод с первой попытки?"]
    random.shuffle(message_question)
    bot.send_message(message.chat.id, f"{message_question[0]} \n ⭐ {rus_word} ⭐:", reply_markup=markup)
    BaseETLBot.add_victory(message.from_user.id, rus_word, eng_word)


@bot.message_handler(func=lambda message: message.text == Command.add_word.text)
def add_word(message):
    """Добавляю слова"""
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    buttons = [Command.back]
    markup.add(*buttons)
    Addword.id_user_word = message.from_user.id
    if Addword.id_add_word == 0:
        bot.send_message(message.chat.id, f"Для добавления слова Вам необходимо ввести слово и его перевод. \n"
                                          f"Ввод слова производите с заглавной буквы",
                         reply_markup=markup)
        bot.send_message(message.chat.id, f"Введите слово на русском языке "
                                          f"и отправьте сообщение: 📝")
    else:
        bot.send_message(message.chat.id, f"Введите перевод слова на английском языке и "
                                          f"отправьте сообщение: 📝", reply_markup=markup)
    bot.register_next_step_handler(message, send_add_word)


def send_add_word(message):
    """Заливка нового слова"""
    rus_word = set('абвгдеёжзийклмнопрстуфхцчшщъыьэюя')
    eng_word = set('abcdefghijklmnopqrstuvwxyz')
    regex = r'[\W\d]+'
    if message.text == Command.back.text:
        Addword.id_add_word = 0
        start_of_studies(message)
    elif Addword.id_add_word == 0:
        if (len(message.text) < 2 or message.text[0].islower()
                                or bool(re.search(regex, message.text))
                                or not message.text[1::].islower()
                                or message.text[1] not in rus_word):
            bot.send_message(message.chat.id, f"Внимательнее к требованиям заполнения! "
                                              f"Слова начинаются с Заглавной буквы."
                                              f"Слово должно быть введено на русском языке")
            Addword.id_add_word = 0
            start_of_studies(message)
        else:
            Addword.new_rus_word = message.text
            result = BaseETLBot.get_check_word(Addword.id_user_word, Addword.new_rus_word)
            if result > 0:
                bot.send_message(message.chat.id, f"Слово 🇷🇺 {Addword.new_rus_word} уже есть в базе знаний ")
                add_word(message)
            else:
                Addword.id_add_word = 1
                add_word(message)
    else:
        if (len(message.text) < 2 or message.text[0].islower()
                                  or bool(re.search(regex, message.text))
                                  or not message.text[1::].islower()
                                  or message.text[1] not in eng_word):
            bot.send_message(message.chat.id, f"Внимательнее к требованиям заполнения! "
                                              f"Слова начинаются с Заглавной буквы."
                                              f"Слово должно быть введено на английском языке")
            Addword.id_add_word = 0
            start_of_studies(message)
        else:
            Addword.new_eng_word = message.text
            Addword.id_add_word = 0
            BaseETLBot.add_word_db(Addword.id_user_word, Addword.new_rus_word, Addword.new_eng_word)
            bot.send_message(message.chat.id, f"Успешно добалено слово 🇷🇺 {Addword.new_rus_word} и \n"
                                              f"перевод 🏴󠁧󠁢󠁥󠁮󠁧󠁿󠁧󠁢󠁥󠁮󠁧󠁿󠁧󠁢󠁥󠁮󠁧󠁿 󠁧󠁢󠁥󠁮󠁧󠁿{Addword.new_eng_word}")


@bot.message_handler(func=lambda message: message.text == Command.back.text)
def send_cancel_word(message):
    """Возврат"""
    start_of_studies(message)


@bot.message_handler(func=lambda message: message.text == Command.my_word.text)
def my_word_list(message):
    """Получаю список своих слов"""
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    buttons = [Command.back]
    markup.add(*buttons)
    bot.send_message(message.chat.id, f"Вот Список Добавленных Вами слов: "
                                      f"📜{BaseETLBot.get_my_word(message.from_user.id)}📜", reply_markup=markup)
    bot.send_message(message.chat.id, f"Для удаления введите слово из списка и отправьте сообщение")
    bot.register_next_step_handler(message, del_word)


@bot.message_handler(func=lambda message: message.text == Command.my_experience.text)
def my_experience(message):

    """Отображение статистики изучения слов"""
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    buttons = [Command.back]
    markup.add(*buttons)
    bot.send_message(message.chat.id,
                     f"Ваш прогресс изучения слов - "
                     f"{BaseETLBot.get_experience(message.from_user.id)} 🥳 (количество изученных слов)",
                     reply_markup=markup)


def del_word(message):
    """Удаление слов или назад в меню"""
    if message.text == Command.back.text:
        start_of_studies(message)
    else:
        new_rus_word = message.text
        bot.send_message(message.chat.id, BaseETLBot.del_word_db(message.from_user.id, new_rus_word))


@bot.message_handler(func=lambda message: message.text == Command.next_word.text)
def next_word(message):
    """Загружаю новый лист слов"""
    start_of_studies(message)


@bot.message_handler(func=lambda message: True, content_types=['text'])
def message_reply(message):
    """Проверка решения"""
    result = BaseETLBot.check_victory(message.from_user.id)
    Addword.id_user_word = message.from_user.id
    Addword.new_eng_word = message.text    
    message_win = ["А Вы молодец 🧡. Верно ✅",
                   "У Вас отлично выходит 🧡. Правильно ✅",
                   "Вы великолепны 🧡. Так точно ✅",
                   "Вы бесспорно правы ✅",
                   "Безупречно 🧡. Угадали ✅",
                   "Очередной успех ✅",
                   "Верно, продолжай ✅",
                   "Отлично, Вы правы ✅",
                   "Безупречно ✅",
                   "Супер. Все правильно ✅"]
    random.shuffle(message_win)

    message_lose = ["Увы ошибка 🙁, но не расстраивайтесь и попробуйте ещё раз ✅",
                    "Ошиблись 🙄, повторите попытку ✅ или нажмите далее ⏩",
                    "Вы были очень близки к верному переводу 🙃",
                    "Попытка не пытка 😘. Продолжайте ✅",
                    "Ой Ой, чуть чуть не так. Ещё раз? ✅",
                    "Не сдавайтесь, всё получится ✅",
                    "На ошибках учатся. Ещё разок ✅",
                    "У Вас точно получится. Попытайтесь ещё ✅",
                    "Ну ничего сташного .....😀 ✅",
                    "Каждая ошибка приближает к победе 💪",
                    "Верный ответ где-то рядом 😜"]
    random.shuffle(message_lose)
    try:
        if message.text == result[0]:
            bot.send_message(message.chat.id, f"{message_win[0]}")
            bot.send_message(message.chat.id, f"Продолжаем ⏩⏩⏩")
            BaseETLBot.add_experience(Addword.id_user_word, Addword.new_eng_word)
            start_of_studies(message)
        else:
            bot.send_message(message.chat.id, f"{message_lose[0]}")
    except:
        start_of_studies(message)


if __name__ == '__main__':
    print('Бот запущен...')
    bot.polling()
