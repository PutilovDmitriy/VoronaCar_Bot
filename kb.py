import telebot
import nameCategory
#keyboard0 основное меню
keyboard0 = telebot.types.ReplyKeyboardMarkup(True)
keyboard0.row(nameCategory.c01)
keyboard0.row(nameCategory.c02)
keyboard0.row(nameCategory.c03)
keyboard0.row(nameCategory.c04)

#keyboard1 Состояние авто
keyboard1 = telebot.types.ReplyKeyboardMarkup(True, True)
keyboard1.row(nameCategory.c111, nameCategory.c112)
keyboard1.row(nameCategory.c121, nameCategory.c122)
keyboard1.row(nameCategory.c13)
keyboard1.row('/Назад')

# keyboard2 Нужна помощь, проблема
keyboard2 = telebot.types.ReplyKeyboardMarkup()
keyboard2.row(nameCategory.c211, nameCategory.c212, )
keyboard2.row(nameCategory.c221, nameCategory.c222)
keyboard2.row(nameCategory.c23)
keyboard2.row('/Назад')

# keyboard3 FAQ
keyboard3 = telebot.types.ReplyKeyboardMarkup(True)
keyboard3.row(nameCategory.c31)
keyboard3.row(nameCategory.c32)
keyboard3.row(nameCategory.c33)
keyboard3.row(nameCategory.c34)
keyboard3.row(nameCategory.c35)
keyboard3.row(nameCategory.c36)
keyboard3.row(nameCategory.c37)
keyboard3.row(nameCategory.c38)
keyboard3.row(nameCategory.c39)
keyboard3.row(nameCategory.c310)
keyboard3.row(nameCategory.c311)
keyboard3.row(nameCategory.c312)
keyboard3.row(nameCategory.c313)
keyboard3.row(nameCategory.c314)
keyboard3.row(nameCategory.c315)
keyboard3.row(nameCategory.c316)
keyboard3.row('/Назад')

#keyboard 4 Заправка автомобиля
keyboard4 = telebot.types.ReplyKeyboardMarkup(True,True)
keyboard4.row(nameCategory.c41)
keyboard4.row(nameCategory.c42)
keyboard4.row('/Назад')

#keyboard last
keyboardL = telebot.types.ReplyKeyboardMarkup(True)
keyboardL.row('/start')
keyboardL.row('/Назад')
