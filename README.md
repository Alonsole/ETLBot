<b>Привет, Посетитель!</b><br />
Вы зашли на страницу курсового проекта на тему «ТГ-чат-бот «Обучалка английскому языку»»<br />
<img src="https://github.com/Alonsole/ETLBot/blob/main/One.png" width=45% /><br /><br />
✅<b>Описание реализации</b><br />
Telegram-бот для изучения английского языка. <br />
Бот выдаёт рандомное слово на английском и 4ре варианта перевода слова на русский язык.<br /><br />
✅<b>База данных</b><br />
Для работы бота разработаны 4 таблицы SQL: <br />
1.-Users - хранение информации о пользователе. Имя и ID.<br />
2.-Words - база знаний (слов и переводов).<br />
3.-Experience - сохранение статистики верных сопоставлений слов.<br />
4.-Victory - хранение связки верного решения для каждого пользователя. <br />
✅<b>Функции</b><br />
1.-Добавление новых слов для текущего пользователя.<br />
2.-Возможность удаления добавленных слов.<br />
3.-Вывод списка с информацией о добавленных словах.<br />
4.-Отображение статистики обучения.<br />
5.-Справочная информация (помощь).<br />
✅<b>Работа</b><br />
1.-Пользователь проходит однократную регистрацию.<br />
2.-После запуска пользователю выдается вопрос и 4 варианта ответа. Верный вариант только один.<br />
3.-Неограниченное количество попыток.<br />
4.-При верном выборе перевода выводится рандомное сообщение с одобрением. Всего 5ть преднастроенных уведомлений по событию.<br />
5.-В случае ошибки отобразится рандомное сообщение об ошибке. Всего 5ть преднастроенных уведомлений по событию.<br />
6.-Добавление слов проводится без дополнительных кнопок меню. Одно слово за раз. Массового ввода не предусмотрено.<br />
7.-Предусмотрена возможность заменить вопрос. По запросу проходит замена ответов.<br />
8.-Верный вариант перевода размещается рандомно в зоне 4х кнопок.<br />
📄<b>Состав</b><br />
1.-settings - настройки подключения к ДатаБазе Postgresql и Token к ТГ Боту.<br /> 
2.-setup - создание ДатаБазы, заливка Таблиц и наполнение тестовым пакетом слов.<br />
3.-create_db - функция создания ДатаБазы.<br />
4.-create_tables - функция заливки Таблиц в ДатаБазу.<br />
5.-word_base - функция загрузки тестового пакета слов в Таблицу Words.<br />
6.-BaseETLBot - функции обработки Бот - ДатаБаза. <br />
7.-ETLBot - Работа Бота.<br />
8.-dataword.json - 30 тестовых слов для первого запуска Бота.<br />
4.-requirements.txt - Информация о библиотеках, версиях библиотек. Быстрая установка. <br />
✅<b>Версия</b><br />
Бот 1.0.2 от 27.09.2024г.<br />
Написано и проверено на Python 3.12.2. На облачном сервере поднято на 3.8.10<br />
🛠<b>Инструкция по установке</b><br />
1.-Настройте подключение к ДатаБазе Postgresql в скрипте setting и укажите Token ТГ Бота.<br />
2.-Запустите скрипт setup<br />
3.-Бот настроен и готов к запуску главного скрипта - ETLBot<br />
Важно - Все файлы необходимо поместить в одну папку. <br /> 
[Документация](https://github.com/Alonsole/ETLBot/blob/main/Documentation.md)  
⚡Исправления.   
Перезагрузка проекта.  02.09.2024г.  
Добавление проверок для контроля добавления новых слов пользователем. 07.09.2024г.  
Правки документации 21.09.2024г.  
Class Command дополнен блоками текста для удобства расширения или правок. Объединил   
действия назад, следующий набор слов в функции next_word 27.09.2024г.  
Корректировки под Python 3.8.10 - 20.11.2024г.  
Правки Вопросов - 20.11.2024г.  
🙁🙁🙁ОШИБКИ-Важно🙁🙁🙁   
1.-При одновременной регистрации (более одного) отображается имя одно из   
2.-При добавлении слова, слово может добавиться не автору  
💊Лечение ошибок  
1.-Убрать приветсвие по имени и запись имени в базу.  
2.-Отключить функцию добавления слов.  
