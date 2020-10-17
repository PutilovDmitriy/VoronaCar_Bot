import os
import re
import time

import psycopg2
import telebot
from flask import Flask, request

import chatID
import menu
import req
import kb
import nameCategory
import reply

isActiveChat = False

DATABASE_URL = os.environ['DATABASE_URL']
conn = psycopg2.connect(DATABASE_URL, sslmode='require')
cursor = conn.cursor()

token = os.environ['TOKEN']
bot = telebot.TeleBot(token, threaded=False)

bot.remove_webhook()
time.sleep(1)
bot.set_webhook(url="https://" + os.environ['HEROKU_APP_NAME'] + ".herokuapp.com/{}".format(token))

app = Flask(__name__)

@app.route('/api/stop-chat/<stop_id>', methods=['GET', 'POST'])
def send_message(stop_id):
    cursor.execute("""
              UPDATE variables set
                chat = False
            WHERE id_chat = %s""", [stop_id])
    conn.commit()
    return "ok", 200

@app.route('/{}'.format(token), methods=['POST'])
def webhook():
    bot.process_new_updates([telebot.types.Update.de_json(request.stream.read().decode("utf-8"))])
    return "ok", 200


@bot.message_handler(commands=['start'])
def start_message(message):
    cursor.execute("""INSERT INTO variables
                (id_chat, start, kb1, kb2,  kb3, kb4,  kb4_2, kb111, kb112, kb121, kb122, kb13, kb13_1, kb211, kb212, kb221, kb222, kb317, number_auto, tel, condition)
                VALUES (%s, True, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, 'a888aa', '1234567890',  'norm' )
                ON CONFLICT (id_chat)
                DO UPDATE SET
                start = True,
                kb1 = False,
                kb2 = False,
                kb3 = False,
                kb4 = False,
                kb4_2 = False,
                kb111 = False,
                kb112 = False,
                kb121 = False,
                kb122 = False,
                kb13 = False,
                kb13_1 = False,
                kb211 = False,
                kb212 = False,
                kb221 = False,
                kb222 = False,
                kb317 = False,
                number_auto = 'a888aa',
                tel = '1234567890',
                condition = 'norm',
                chat = False""",
                   [message.chat.id])
    conn.commit()
    bot.send_message(message.chat.id, reply.start, reply_markup=kb.keyboard0)


@bot.message_handler(commands=['Назад'])
def back_message(message):
    # Получение данных из бд
    cursor.execute("""SELECT * from variables where id_chat = %s""", [message.chat.id])
    rows = cursor.fetchall()
    for row in rows:
        # Первое меню
        menu.start = row[1]
        menu.kb1 = row[2]
        menu.kb2 = row[3]
        menu.kb3 = row[4]
        menu.kb4 = row[5]
        menu.kb4_2 = row[6]
        menu.kb111 = row[7]
        menu.kb112 = row[8]
        menu.kb121 = row[9]
        menu.kb122 = row[10]
        menu.kb13 = row[11]
        menu.kb13_1 = row[12]
        menu.kb211 = row[13]
        menu.kb212 = row[14]
        menu.kb221 = row[15]
        menu.kb222 = row[16]
        menu.kb317 = row[17]
        menu.number_auto = row[18]
        menu.tel = row[19]
        menu.condition = row[20]
    if menu.start:
        cursor.execute("""
          UPDATE variables set
                kb1 = False,
                kb2 = False,
                kb3 = False,
                kb4 = False,
                kb4_2 = False,
                kb111 = False,
                kb112 = False,
                kb121 = False,
                kb122 = False,
                kb13 = False,
                kb13_1 = False,
                kb211 = False,
                kb212 = False,
                kb221 = False,
                kb222 = False,
                kb317 = False,
                tel = '1234567890',
                number_auto = 'a888aa',
                condition = 'norm'
        WHERE id_chat = %s""", [message.chat.id])
        conn.commit()
        bot.send_message(message.chat.id, reply.start, reply_markup=kb.keyboard0)
    elif menu.kb1:
        cursor.execute("""
          UPDATE variables set
            kb111 = False
            kb112 = False
            kb121 = False
            kb122 = False
        WHERE id_chat = %s""", [message.chat.id])
        conn.commit()
        # menu.kb111 = False
        # menu.kb112 = False
        # menu.kb121 = False
        # menu.kb122 = False
        bot.send_message(message.chat.id, reply.r01, reply_markup=kb.keyboard1)
    elif menu.kb111 or menu.kb112 or menu.kb121 or menu.kb122 or menu.kb13:
        cursor.execute("""UPDATE variables set
            start = True,
            kb1 = True
        where id_chat = %s""", [message.chat.id])
        conn.commit()
        # menu.start = True
        # menu.kb1 = True
        bot.send_message(message.chat.id, reply.R1, reply_markup=kb.keyboardL)
    elif menu.kb13_1:
        cursor.execute("""UPDATE variables set
            kb13 = True,
            kb13_1 = False
        where id_chat = %s""", [message.chat.id])
        conn.commit()
        # menu.kb13 = True
        # menu.kb13_1 = False
        bot.send_message(message.chat.id, reply.R1_1, reply_markup=kb.keyboardL)
    elif menu.kb211 or menu.kb212 or menu.kb221 or menu.kb222 == True:
        cursor.execute("""UPDATE variables set
            start = True,
            kb2 = True,
            kb211 = False,
            kb212 = False,
            kb221 = False,
            kb222 = False
        where id_chat = %s""", [message.chat.id])
        conn.commit()
        # menu.start = True
        # menu.kb2 = True
        # menu.kb211 = False
        # menu.kb212 = False
        # menu.kb221 = False
        # menu.kb222 = False
        bot.send_message(message.chat.id, reply.r02, reply_markup=kb.keyboard2)
    elif menu.kb317:
        cursor.execute("""UPDATE variables set
            kb317 = False,
            start = True
        where id_chat = %s""", [message.chat.id])
        conn.commit()
        # menu.kb317 = False
        # menu.start = True
        bot.send_message(message.chat.id, reply.r03, reply_markup=kb.keyboard3)
    elif menu.kb4:
        cursor.execute("""UPDATE variables set
            kb4 = False,
            start = True
        where id_chat = %s""", [message.chat.id])
        conn.commit()
        # menu.kb4 = False
        # menu.start = True
        bot.send_message(message.chat.id, reply.start, reply_markup=kb.keyboard4)
    elif menu.kb4_2:
        cursor.execute("""UPDATE variables set
            kb4_2 = False,
            kb4 = True
        where id_chat = %s""", [message.chat.id])
        conn.commit()
        # menu.kb4_2 = False
        # menu.kb4 = True
        bot.send_message(message.chat.id, reply.r42, reply_markup=kb.keyboard4)
    else:
        bot.send_message(message.chat.id, "Error")


@bot.message_handler(content_types=['text'])
def handle_text(message):
    # Получение данных из бд
    cursor.execute("""SELECT * from variables where id_chat = %s""", [message.chat.id])
    rows = cursor.fetchall()
    for row in rows:
        # Первое меню
        menu.start = row[1]
        menu.kb1 = row[2]
        menu.kb2 = row[3]
        menu.kb3 = row[4]
        menu.kb4 = row[5]
        menu.kb4_2 = row[6]
        menu.kb111 = row[7]
        menu.kb112 = row[8]
        menu.kb121 = row[9]
        menu.kb122 = row[10]
        menu.kb13 = row[11]
        menu.kb13_1 = row[12]
        menu.kb211 = row[13]
        menu.kb212 = row[14]
        menu.kb221 = row[15]
        menu.kb222 = row[16]
        menu.kb317 = row[17]
        menu.number_auto = row[18]
        menu.tel = row[19]
        menu.condition = row[20]
        isActiveChat = row[21]
    if message.text == nameCategory.c01:
        bot.send_message(message.chat.id, reply.r01, reply_markup=kb.keyboard1)
    elif message.text == nameCategory.c02:
        bot.send_message(message.chat.id, reply.r02, reply_markup=kb.keyboard2)
    elif message.text == nameCategory.c03:
        bot.send_message(message.chat.id, reply.r03, reply_markup=kb.keyboard3)
    elif message.text == nameCategory.c04:
        bot.send_message(message.chat.id, reply.r04, reply_markup=kb.keyboard4)

    # keyboard1 Состояние авто
    elif message.text == nameCategory.c111:
        cursor.execute("""UPDATE variables set
            kb1 = True,
            kb111 = True,
            kb112 = False,
            kb121 = False,
            kb122 = False,
            kb13 = False
        where id_chat = %s""", [message.chat.id])
        conn.commit()
        # menu.kb1 = True
        # menu.kb111 = True
        # menu.kb112 = False
        # menu.kb121 = False
        # menu.kb122 = False
        # menu.kb13 = False
        bot.send_message(message.chat.id, reply.R1)
    elif message.text == nameCategory.c112:
        cursor.execute("""UPDATE variables set
            kb1 = True,
            kb112 = True,
            kb111 = False,
            kb121 = False,
            kb122 = False,
            kb13 = False
        where id_chat = %s""", [message.chat.id])
        conn.commit()
        # menu.kb1 = True
        # menu.kb112 = True
        # menu.kb111 = False
        # menu.kb121 = False
        # menu.kb122 = False
        # menu.kb13 = False
        bot.send_message(message.chat.id, reply.R1)
    elif message.text == nameCategory.c121:
        cursor.execute("""UPDATE variables set
            kb1 = True,
            kb121 = True,
            kb111 = False,
            kb112 = False,
            kb122 = False,
            kb13 = False
        where id_chat = %s""", [message.chat.id])
        conn.commit()
        # menu.kb1 = True
        # menu.kb121 = True
        # menu.kb111 = False
        # menu.kb112 = False
        # menu.kb122 = False
        # menu.kb13 = False
        bot.send_message(message.chat.id, reply.R1)
    elif message.text == nameCategory.c122:
        cursor.execute("""UPDATE variables set
            kb1 = True,
            kb122 = True,
            kb111 = False,
            kb112 = False,
            kb121 = False,
            kb13 = False
        where id_chat = %s""", [message.chat.id])
        conn.commit()
        # menu.kb1 = True
        # menu.kb122 = True
        # menu.kb111 = False
        # menu.kb112 = False
        # menu.kb121 = False
        # menu.kb13 = False
        bot.send_message(message.chat.id, reply.R1)
    elif message.text == nameCategory.c13:
        cursor.execute("""UPDATE variables set
            kb1 = True,
            kb13 = True,
            kb111 = False,
            kb112 = False,
            kb121 = False,
            kb122 = False
        where id_chat = %s""", [message.chat.id])
        conn.commit()
        # menu.kb1 = True
        # menu.kb13 = True
        # menu.kb111 = False
        # menu.kb112 = False
        # menu.kb121 = False
        # menu.kb122 = False
        bot.send_message(message.chat.id, reply.R1)

    # keyboard1 обработчик номера телефона
    elif menu.kb1:
        if re.match(r'[7-8]{1}[0-9]{10}', message.text) or re.match(r'[+]{1}[7-8]{1}[0-9]{10}', message.text):
            cursor.execute("""UPDATE variables set
                kb1 = False,
                start = False,
                tel = %s
            where id_chat = %s""", [message.text, message.chat.id])
            conn.commit()
            # menu.kb1 = False
            # menu.start = False
            # menu.tel = message.text
            bot.send_message(message.chat.id, reply.R1_1, reply_markup=kb.keyboardL)
        else:
            bot.send_message(message.chat.id, reply.tel)
    # Номер авто
    # 1 - 4
    elif menu.kb111:
        if re.match(r'[a-zA-Zа-яА-Я]{1}[0-9]{3}[a-zA-Zа-яА-Я]{2}', message.text):
            cursor.execute("""UPDATE variables set
                kb111 = False,
                start = True,
                number_auto = 'a888a',
                tel = '1234567890'
            where id_chat = %s""", [message.chat.id])
            conn.commit()
            # menu.kb111 = False
            # menu.start = True
            menu.number_auto = message.text
            bot.send_message(message.chat.id, reply.r1send, reply_markup=kb.keyboard0)
            bot.send_message(chatID.Vorona, (
                    nameCategory.c111 + " автомобиля c номером " + menu.number_auto + " (Тел: " + menu.tel + ")"))
            # menu.number_auto = ""
            # menu.tel = ""
        else:
            bot.send_message(message.chat.id, reply.number)

    elif menu.kb112:
        if re.match(r'[a-zA-Zа-яА-Я]{1}[0-9]{3}[a-zA-Zа-яА-Я]{2}', message.text):
            cursor.execute("""UPDATE variables set
                kb112 = False,
                start = True,
                number_auto = 'a888a',
                tel = '1234567890'
            where id_chat = %s""", [message.chat.id])
            conn.commit()
            # menu.kb112 = False
            # menu.start = True
            menu.number_auto = message.text
            bot.send_message(message.chat.id, reply.r1send, reply_markup=kb.keyboard0)
            bot.send_message(chatID.Vorona, (
                    nameCategory.c112 + " автомобиля c номером " + menu.number_auto + " (Тел: " + menu.tel + ")"))
            # menu.number_auto = ""
            # menu.tel = ""
        else:
            bot.send_message(message.chat.id, reply.number)

    elif menu.kb121:
        if re.match(r'[a-zA-Zа-яА-Я]{1}[0-9]{3}[a-zA-Zа-яА-Я]{2}', message.text):
            cursor.execute("""UPDATE variables set
                kb121 = False,
                start = True,
                number_auto = 'a888a',
                tel = '1234567890'
            where id_chat = %s""", [message.chat.id])
            conn.commit()
            # menu.kb121 = False
            # menu.start = True
            menu.number_auto = message.text
            bot.send_message(message.chat.id, reply.r1send, reply_markup=kb.keyboard0)
            bot.send_message(chatID.Vorona, (
                    nameCategory.c121 + " у автомобиля c номером " + menu.number_auto + " (Тел: " + menu.tel + ")"))
            # menu.number_auto = ""
            # menu.tel = ""
        else:
            bot.send_message(message.chat.id, reply.number)

    elif menu.kb122:
        if re.match(r'[a-zA-Zа-яА-Я]{1}[0-9]{3}[a-zA-Zа-яА-Я]{2}', message.text):
            cursor.execute("""UPDATE variables set
                kb122 = False,
                start = True,
                number_auto = 'a888a',
                tel = '1234567890'
            where id_chat = %s""", [message.chat.id])
            conn.commit()
            # menu.kb122 = False
            # menu.start = True
            menu.number_auto = message.text
            bot.send_message(message.chat.id, reply.r1send, reply_markup=kb.keyboard0)
            bot.send_message(chatID.Vorona, (
                    nameCategory.c122 + " в автомобиле c номером " + menu.number_auto + " (Тел: " + menu.tel + ")"))
            # menu.number_auto = ""
            # menu.tel = ""
        else:
            bot.send_message(message.chat.id, reply.number)

    # 5 Описание проблемы
    elif menu.kb13:
        if re.match(r'[a-zA-Zа-яА-Я]{1}[0-9]{3}[a-zA-Zа-яА-Я]{2}', message.text):
            cursor.execute("""UPDATE variables set
                kb13 = False,
                kb13_1 = True,
                number_auto = %s
            where id_chat = %s""", [message.text, message.chat.id])
            conn.commit()
            # menu.kb13 = False
            # menu.kb13_1 = True
            # menu.number_auto = message.text
            bot.send_message(message.chat.id, reply.r13)
        else:
            bot.send_message(message.chat.id, reply.number)

    elif menu.kb13_1:
        cursor.execute("""UPDATE variables set
            kb13_1 = False,
            start = True,
            tel = '1234567890'
            number_auto = 'a888a'
            condition = 'norm'
        where id_chat = %s""", [message.text, message.chat.id])
        conn.commit()
        # menu.kb13_1 = False
        # menu.start = True
        menu.condition = message.text
        bot.send_message(message.chat.id, reply.r1send, reply_markup=kb.keyboard1)
        bot.send_message(chatID.Vorona, (
                "Автомобиль c номером " + menu.number_auto + " (Тел: " + menu.tel + ") /// " + menu.condition))
        # menu.tel = ""
        # menu.number_auto = ""
        # menu.condition = ""

    # keyboard2 Нужна помощь, проблема
    elif message.text == nameCategory.c211:
        cursor.execute("""UPDATE variables set
            kb211 = True,
            start = False,
            number_auto = %s
         where id_chat = %s""", [message.text, message.chat.id])
        conn.commit()
        # menu.kb211 = True
        # menu.start = False
        bot.send_message(message.chat.id, reply.R2, reply_markup=kb.keyboardL)
    elif message.text == nameCategory.c212:
        cursor.execute("""UPDATE variables set
            kb212 = True,
            start = False,
            number_auto = %s
        where id_chat = %s""", [message.text, message.chat.id])
        conn.commit()
        # menu.kb212 = True
        # menu.start = False
        bot.send_message(message.chat.id, reply.R2, reply_markup=kb.keyboardL)
    elif message.text == nameCategory.c221:
        cursor.execute("""UPDATE variables set
            kb221 = True,
            start = False,
            number_auto = %s
        where id_chat = %s""", [message.text, message.chat.id])
        conn.commit()
        # menu.kb221 = True
        # menu.start = False
        bot.send_message(message.chat.id, reply.R2, reply_markup=kb.keyboardL)
    elif message.text == nameCategory.c222:
        cursor.execute("""UPDATE variables set
            kb222 = True,
            start = False,
            number_auto = %s
        where id_chat = %s""", [message.text, message.chat.id])
        conn.commit()
        # menu.kb222 = True
        # menu.start = False
        bot.send_message(message.chat.id, reply.R2, reply_markup=kb.keyboardL)
    elif message.text == nameCategory.c23:
        bot.send_message(message.chat.id, "+79026324545", reply_markup=kb.keyboard0)
    # keyboard2 обработчик номера телефона
    elif menu.kb211:
        if re.match(r'[7-8]{1}[0-9]{10}', message.text) or re.match(r'[+]{1}[7-8]{1}[0-9]{10}', message.text):
            cursor.execute("""UPDATE variables set
                kb211 = False,
                start = True
            where id_chat = %s""", [message.chat.id])
            conn.commit()
            # menu.kb211 = False
            # menu.start = True
            bot.send_message(message.chat.id, reply.r2send, reply_markup=kb.keyboard0)
            bot.send_message(chatID.Vorona, nameCategory.c211 + " " + message.text)
        else:
            bot.send_message(message.chat.id, reply.tel)
    elif menu.kb212:
        if re.match(r'[7-8]{1}[0-9]{10}', message.text) or re.match(r'[+]{1}[7-8]{1}[0-9]{10}', message.text):
            cursor.execute("""UPDATE variables set
                kb212 = False,
                start = True
            where id_chat = %s""", [message.chat.id])
            conn.commit()
            # menu.kb212 = False
            # menu.start = True
            bot.send_message(message.chat.id, reply.r2send, reply_markup=kb.keyboard0)
            bot.send_message(chatID.Vorona, nameCategory.c212 + " " + message.text)
        else:
            bot.send_message(message.chat.id, reply.tel)
    elif menu.kb221:
        if re.match(r'[7-8]{1}[0-9]{10}', message.text) or re.match(r'[+]{1}[7-8]{1}[0-9]{10}', message.text):
            cursor.execute("""UPDATE variables set
                kb221 = False,
                start = True
            where id_chat = %s""", [message.chat.id])
            conn.commit()
            # menu.kb221 = False
            # menu.start = True
            bot.send_message(message.chat.id, reply.r2send, reply_markup=kb.keyboard0)
            bot.send_message(chatID.Vorona, nameCategory.c221 + " " + message.text)
        else:
            bot.send_message(message.chat.id, reply.tel)
    elif menu.kb222:
        if re.match(r'[7-8]{1}[0-9]{10}', message.text) or re.match(r'[+]{1}[7-8]{1}[0-9]{10}', message.text):
            cursor.execute("""UPDATE variables set
                kb222 = False,
                start = True
            where id_chat = %s""", [message.chat.id])
            conn.commit()
            # menu.kb222 = False
            # menu.start = True
            bot.send_message(message.chat.id, reply.r2send, reply_markup=kb.keyboard0)
            bot.send_message(chatID.Vorona, nameCategory.c222 + " " + message.text)
        else:
            bot.send_message(message.chat.id, reply.tel)
    # keyboard3 FAQ
    elif message.text == nameCategory.c31:
        bot.send_message(message.chat.id, reply.r31)
    elif message.text == nameCategory.c32:
        bot.send_message(message.chat.id, reply.r32)
    elif message.text == nameCategory.c33:
        bot.send_message(message.chat.id, reply.r33)
    elif message.text == nameCategory.c34:
        bot.send_message(message.chat.id, reply.r34)
    elif message.text == nameCategory.c35:
        bot.send_message(message.chat.id, reply.r35)
    elif message.text == nameCategory.c36:
        bot.send_message(message.chat.id, reply.r36)
    elif message.text == nameCategory.c37:
        bot.send_message(message.chat.id, reply.r37)
    elif message.text == nameCategory.c38:
        bot.send_message(message.chat.id, reply.r38)
    elif message.text == nameCategory.c39:
        bot.send_message(message.chat.id, reply.r39)
    elif message.text == nameCategory.c310:
        bot.send_message(message.chat.id, reply.r310)
    elif message.text == nameCategory.c311:
        bot.send_message(message.chat.id, reply.r311)
    elif message.text == nameCategory.c312:
        bot.send_message(message.chat.id, reply.r312)
    elif message.text == nameCategory.c313:
        bot.send_message(message.chat.id, reply.r313)
    elif message.text == nameCategory.c314:
        bot.send_message(message.chat.id, reply.r314)
    elif message.text == nameCategory.c315:
        bot.send_message(message.chat.id, reply.r315)
    elif message.text == nameCategory.c316:
        bot.send_message(message.chat.id, reply.r316)
    elif message.text == nameCategory.c317:
        cursor.execute("""UPDATE variables set
            kb317 = True,
            start = False
        where id_chat = %s""", [message.chat.id])
        conn.commit()
        # menu.kb317 = True
        # menu.start = False
        bot.send_message(message.chat.id, reply.r317, reply_markup=kb.keyboardL)
    elif menu.kb317:
        cursor.execute("""UPDATE variables set
            kb317 = False,
            start = True,
            chat = True
        where id_chat = %s""", [message.chat.id])
        conn.commit()
        # menu.kb317 = False
        # menu.start = True
        bot.send_message(message.chat.id, reply.r3_17)
        req.send_data(message.chat.id, message.text, message.from_user.first_name)


    # keyboard 4 Заправка автомобиля
    elif message.text == nameCategory.c41:
        cursor.execute("""UPDATE variables set
            kb4 = False
        where id_chat = %s""", [message.chat.id])
        conn.commit()
        # menu.kb4 = False
        bot.send_message(message.chat.id, reply.r41)
    elif message.text == nameCategory.c42:
        cursor.execute("""UPDATE variables set
            kb4 = True
        where id_chat = %s""", [message.chat.id])
        conn.commit()
        # menu.kb4 = True
        bot.send_message(message.chat.id, reply.r42)
    elif menu.kb4:
        if re.match(r'[7-8]{1}[0-9]{10}', message.text) or re.match(r'[+]{1}[7-8]{1}[0-9]{10}', message.text):
            cursor.execute("""UPDATE variables set
                kb4 = False,
                start = False,
                kb4_2 = True,
                tel = %s
            where id_chat = %s""", [message.text, message.chat.id])
            conn.commit()
            # menu.kb4 = False
            # menu.start = False
            # menu.kb4_2 = True
            # menu.tel = message.text
            bot.send_message(message.chat.id, reply.r4_2, reply_markup=kb.keyboardL)
        else:
            bot.send_message(message.chat.id, reply.tel)
    elif menu.kb4_2:
        bot.send_message(message.chat.id, reply.r4_2)
    elif isActiveChat:
        req.send_data(message.chat.id, message.text, message.from_user.first_name)
    # ELSE
    else:
        bot.send_message(message.chat.id,
                         'Пожалуйста, используйте меню для доступа к моим функциям. Выберите интересующий вас пункт.')


@bot.message_handler(content_types=['photo', 'document'])
def handle_docs_audio(message):
    # Получение данных из бд
    cursor.execute("""SELECT * from variables where id_chat = %s""", [message.chat.id])
    rows = cursor.fetchall()
    for row in rows:
        # Первое меню
        menu.start = row[1]
        menu.kb1 = row[2]
        menu.kb2 = row[3]
        menu.kb3 = row[4]
        menu.kb4 = row[5]
        menu.kb4_2 = row[6]
        menu.kb111 = row[7]
        menu.kb112 = row[8]
        menu.kb121 = row[9]
        menu.kb122 = row[10]
        menu.kb13 = row[11]
        menu.kb13_1 = row[12]
        menu.kb211 = row[13]
        menu.kb212 = row[14]
        menu.kb221 = row[15]
        menu.kb222 = row[16]
        menu.kb317 = row[17]
        menu.number_auto = row[18]
        menu.tel = row[19]
        menu.condition = row[20]
    if menu.kb4_2:
        cursor.execute("""UPDATE variables set
            kb4_2 = False,
            start = True
        where id_chat = %s""", [message.chat.id])
        conn.commit()
        # menu.kb4_2 = False
        # menu.start = True
        bot.send_message(message.chat.id, reply.r4send, reply_markup=kb.keyboard4)
        bot.send_message(chatID.Vorona, menu.tel)
        bot.forward_message(chatID.Vorona, message.chat.id, message.message_id)
if __name__ == "__main__":
  app.run()
