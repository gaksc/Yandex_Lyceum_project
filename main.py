# -*- coding: utf-8 -*-
import telebot
from telebot import types
from config import BOT_TOKEN
import os
import platform
import json
import requests
from io import BytesIO
from PIL import Image, ImageGrab
import time
import webbrowser
import sqlite3
action = ''
con = sqlite3.connect("users.db", check_same_thread=False)
cur = con.cursor()
idk = cur.execute("""SELECT id FROM users""").fetchall()
ids = []
rights = open('authorized.txt', 'a+')
rights.flush()
authorized = open("authorized.txt","r").readlines()
authorized = [i.strip() for i in authorized]
your_id = 1
for i in idk:
    ids.append(i[0])
def check(message):
    global ids, idk
    if message.chat.id not in ids:
        first = message.chat.first_name
        last = message.chat.last_name
        id = message.chat.id
        sql = f"""INSERT INTO users (id, first_name, last_name) VALUES ({id}, '{first}', '{last}')"""
        cur.execute(sql)
        con.commit()
        ids = []
        idk = cur.execute("""SELECT id FROM users""").fetchall()
        for i in idk:
            ids.append(i[0])


bot_token = BOT_TOKEN
bot = telebot.TeleBot(bot_token)

@bot.message_handler(commands=['start'])
def send_welcome(message):
    try:
        check(message)
        if str(message.chat.id) == '6225765339':
            markup = telebot.types.ReplyKeyboardMarkup(resize_keyboard=True)
            btn0 = telebot.types.KeyboardButton("/authorize")
            btn1 = telebot.types.KeyboardButton("/unauthorize")
            btn2 = telebot.types.KeyboardButton("/restart")
            btn3 = telebot.types.KeyboardButton("/sleep")
            btn4 = telebot.types.KeyboardButton("/info")
            btn5 = telebot.types.KeyboardButton("/screenshot")
            btn6 = telebot.types.KeyboardButton("/who")
            btn7 = telebot.types.KeyboardButton("/fish")
            btn8 = telebot.types.KeyboardButton("/shutdown")
            btn9 = telebot.types.KeyboardButton("/help")
            markup.add(btn0, btn1, btn2, btn3, btn4, btn5, btn6, btn7, btn8, btn9)
            bot.reply_to(message, "Welcome! Use /help for a list of commands.", reply_markup=markup)
        else:
            markup = telebot.types.ReplyKeyboardMarkup(resize_keyboard=True)
            btn0 = telebot.types.KeyboardButton("/help")
            btn1 = telebot.types.KeyboardButton("/shutdown")
            btn2 = telebot.types.KeyboardButton("/restart")
            btn3 = telebot.types.KeyboardButton("/sleep")
            btn4 = telebot.types.KeyboardButton("/info")
            btn5 = telebot.types.KeyboardButton("/screenshot")
            btn6 = telebot.types.KeyboardButton("/who")
            btn7 = telebot.types.KeyboardButton("/fish")
            markup.add(btn0, btn1, btn2, btn3, btn4, btn5, btn6, btn7)
            bot.reply_to(message, "Welcome! Use /help for a list of commands.", reply_markup=markup)
    except Exception as e:
        time.sleep(2)
        bot.send_message(message.chat.id, 'ERROR ' + str(e))

@bot.message_handler(commands=['help'])
def send_help(message):
    try:
        check(message)
        bot.reply_to(message, "Commands: \n/shutdown - shutdown the computer \n/restart - restart the computer \n/sleep - put the computer to sleep \n /info - information about PC"+
                              "\n/screenshot - Make a screenshot \n/who - Who used this bot \n/fish - Use when fish \n/authorize - Give rights to restart, sleep and shutdown " +
                     "\n/unauthorize - Downgrade rights of users")
    except Exception as e:
        time.sleep(2)
        bot.send_message(message.chat.id, 'ERROR ' + str(e))

@bot.message_handler(commands=['shutdown'])
def shutdown_computer(message):
    try:
        check(message)
        if str(message.chat.id) in authorized:
            os.system("shutdown /s /t 1")
            bot.reply_to(message, "Shutting down the computer...")
        else:
            bot.reply_to(message, "У вас нет прав, админ Никита выдаст")
    except Exception as e:
        time.sleep(2)
        bot.send_message(message.chat.id, 'ERROR ' + str(e))

@bot.message_handler(commands=['restart'])
def restart_computer(message):
    try:
        check(message)
        if str(message.chat.id) in authorized:
            os.system("shutdown /r /t 1")
            bot.reply_to(message, "Restarting the computer...")
        else:
            bot.reply_to(message, "У вас нет прав, админ Никита выдаст")
    except Exception as e:
        time.sleep(2)
        bot.send_message(message.chat.id, 'ERROR ' + str(e))

@bot.message_handler(commands=['sleep'])
def sleep_computer(message):
    try:
        check(message)
        if str(message.chat.id) in authorized:
            os.system("rundll32.exe powrprof.dll,SetSuspendState 0,1,0")
            bot.reply_to(message, "Putting the computer to sleep...")
        else:
            bot.reply_to(message, "У вас нет прав, админ Никита выдаст")
    except Exception as e:
        time.sleep(2)
        bot.send_message(message.chat.id, 'ERROR ' + str(e))

@bot.message_handler(commands=['info'])
def sleep_computers(message):
    try:
        check(message)
        r = requests.get('http://ip.42.pl/raw')
        ip_address = r.text
        request_url = 'https://geolocation-db.com/jsonp/' + ip_address
        response = requests.get(request_url)
        result = response.content.decode()
        result = result.split("(")[1].strip(")")
        result = json.loads(result)
        toponym_longitude = str(result['longitude'])
        toponym_lattitude = str(result['latitude'])
        delta = "0.01"
        map_params = {
            "ll": ",".join([toponym_longitude, toponym_lattitude]),
            "spn": ",".join([delta, delta]),
            "l": "map"
        }
        map_api_server = "http://static-maps.yandex.ru/1.x/"
        response = requests.get(map_api_server, params=map_params)
        a = Image.open(BytesIO(
            response.content))
        a.save('user.png')
        img = open('user.png', 'rb')
        windows = platform.platform()
        processor = platform.processor()
        try:
            user = os.getlogin()
        except Exception:
            user = 'Pycharm'
        bot.send_photo(message.chat.id, img, caption=result['country_name'] + ', ' + result['state'] + ', ' + result['city']
                       + '\n' + 'PC: ' + user + '\nOS: ' + windows + '\nProcessor: ' + processor)
    except Exception as e:
        time.sleep(2)
        bot.send_message(message.chat.id, 'ERROR ' + str(e))

@bot.message_handler(commands=['screenshot'])
def screenshot_computer(message):
    try:
        check(message)
        img = ImageGrab.grab()
        img.save("screen.jpg")
        img = open('screen.jpg', 'rb')
        bot.send_photo(message.chat.id, img, caption='ДОББИ ПРИНЕСТИ СКРИНШОТ')
    except Exception as e:
        time.sleep(2)
        bot.send_message(message.chat.id, 'ERROR ' + str(e))

@bot.message_handler(commands=['who'])
def who(message):
    try:
        nres = 'id, first_name, last_name \n'
        check(message)
        result = cur.execute("""SELECT * FROM users""").fetchall()
        for i in result:
            nres += str(i[0]) + ' ' + str(i[1]) + ' ' + str(i[2]) + '\n'
        bot.send_message(message.chat.id, nres)
    except Exception as e:
        time.sleep(2)
        bot.send_message(message.chat.id, 'ERROR ' + str(e))

@bot.message_handler(commands=['fish'])
def fish(message):
    try:
        check(message)
        webbrowser.open_new_tab('https://www.youtube.com/watch?v=gnzYZ_6RmgA')
        time.sleep(1)
        os.startfile(r'2.jpg')
    except Exception as e:
        time.sleep(2)
        bot.send_message(message.chat.id, 'ERROR ' + str(e))

@bot.message_handler(commands=['authorize'])
def giverights(message):
    try:
        global your_id, action
        check(message)
        action = 'authorize'
        if str(message.chat.id) == '6225765339':
            markup = types.InlineKeyboardMarkup()
            result = cur.execute("""SELECT * FROM users""").fetchall()
            for i in result:
                button1 = types.InlineKeyboardButton(str(i[1]) + ' ' + str(i[2]), callback_data=str(i[0]))
                markup.add(button1)
            bot.send_message(message.chat.id, 'Кому выдать права?', reply_markup=markup)
            your_id = message.chat.id

        else:
            bot.reply_to(message, "Права не выросли, чтобы авторизировать")

    except Exception as e:
        time.sleep(2)
        bot.send_message(message.chat.id, 'ERROR ' + str(e))


@bot.message_handler(commands=['unauthorize'])
def notgiverights(message):
    try:
        global your_id, action
        check(message)
        action = 'unauthorize'
        if str(message.chat.id) == '6225765339':
            markup = types.InlineKeyboardMarkup()
            result = cur.execute("""SELECT * FROM users""").fetchall()
            for i in result:
                button1 = types.InlineKeyboardButton(str(i[1]) + ' ' + str(i[2]), callback_data=str(i[0]))
                markup.add(button1)
            bot.send_message(message.chat.id, 'У кого отнять права?', reply_markup=markup)
            your_id = message.chat.id

        else:
            bot.reply_to(message, "Права не выросли, чтобы авторизировать")

    except Exception as e:
        time.sleep(2)
        bot.send_message(message.chat.id, 'ERROR ' + str(e))


@bot.callback_query_handler(func=lambda call:True)
def callback_query(call):
    global your_id, authorized, rights, action
    req = call.data.split('_')
    idf = req[0]
    if action == 'authorize':
        if str(idf) not in authorized:
            rights.write('\n' + str(idf) + '\n')
            rights.flush()
            authorized = open("authorized.txt", "r").readlines()
            authorized = [i.strip() for i in authorized]
            bot.send_message(your_id, 'Успешно!')
        else:
            bot.send_message(your_id, 'Упс, id ' + str(idf) + ' уже админ')
    elif action == 'unauthorize':
        if str(idf) in authorized:
            authorized.remove(str(idf))
            open("authorized.txt", "w").write('\n'.join(authorized))
            rights.flush()
            authorized = open("authorized.txt", "r").readlines()
            authorized = [i.strip() for i in authorized]
            bot.send_message(your_id, 'Успешно!')
        else:
            bot.send_message(your_id, 'Упс, id ' + str(idf) + ' не имеет админ прав')
bot.polling()