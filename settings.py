import telebot
from sqlalchemy.orm import declarative_base

Base = declarative_base()

DATABASES = {
    'postgresql': {
        'NAME': 'postgresql',
        'USER': 'postgres',
        'PASSWORD': '1234',
        'HOST': 'localhost',
        'PORT': '5432',
        'BD_NAME': 'etlbase',
    }
}

data_bd = DATABASES['postgresql']
PATH = (f"{data_bd['NAME']}://{data_bd['USER']}:{data_bd['PASSWORD']}@"
        f"{data_bd['HOST']}:{data_bd['PORT']}/{data_bd['BD_NAME']}")

TOKEN = 'TOKEN'
bot = telebot.TeleBot(TOKEN)