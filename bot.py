#!/usr/bin/python
import telebot
from telebot import types
import logging
from conf import *
from datetime import datetime
import time
import requests
import random
import re

logger = telebot.logger
telebot.logger.setLevel(logging.DEBUG)
logging.basicConfig(filename = "logfile.log",
                    filemode = "w",
                    level = logging.DEBUG)
logger = logging.getLogger()

print(f"\nLaunched Bot..\n")

bot = telebot.TeleBot(TOKEN)

f = open('var_1.txt', 'r', encoding='UTF-8')
var_1 = f.read().split('\n')
f.close()

@bot.message_handler(commands=['start'])
def start(message):
	markup = types.ReplyKeyboardMarkup(row_width=2)
	btn1 = types.KeyboardButton('Узнать Гошу лучше')
	btn2 = types.KeyboardButton('Загадки от Гоши')
	btn3 = types.KeyboardButton('Узнать погоду у Гоши')
	btn4 = types.KeyboardButton('Забашлять Гоше')
	btn5 = types.KeyboardButton('admin_panel')
	markup.add(btn1, btn2, btn3, btn4)
	weekday = weekday_str(message)
	if weekday == "Понедельник":
		weekday = "понедельник 😑"
	if weekday == "Вторник":
		weekday = "вторник 🤔"
	if weekday == "Среда":
		weekday = "среда 🤫"
	if weekday == "Четверг":
		weekday = "четверг 😬"
	if weekday == "Пятница":
		weekday = "пятница 🤤"
	if weekday == "Суббота":
		weekday = "суббота 😆"
	if weekday == "Воскресенье":
		weekday = "воскресенье 😣"
	bot.send_message(message.chat.id, f"<b>Привет {message.from_user.first_name}! Сегодня {weekday}</b>\nЯ буду тебя развлекать, когда тебе одиноко😏", parse_mode='html', reply_markup=markup)
	if message.from_user.first_name == admin_name:
		markup.add(btn5)
		bot.send_message(message.chat.id, f"Login is Allowed in the Admin Panel",  reply_markup=markup)
		
def admin_panel(message):
	if message.from_user.first_name != admin_name:
		start(message)
	else:
		markup_admin = types.ReplyKeyboardMarkup(row_width=1)
		btn_admin = types.KeyboardButton('admin_panel')
		btn_log = types.KeyboardButton('read_logs')
		btn_clear_log = types.KeyboardButton('clear_logs')
		btn_back = types.KeyboardButton('back_to_user')
		markup_admin.add(btn_admin, btn_log, btn_clear_log, btn_back)
		bot.send_message(message.chat.id, f"Приветствую хозяин {message.from_user.first_name}!",  reply_markup=markup_admin)

def read_logs(message):
	f = open('log.txt', 'r', encoding='UTF-8')
	read_file = f.read()
	bot.send_message(message.chat.id, f"{read_file}")
	f.close()

def clear_logs(message):
	f = open('log.txt', 'w', encoding='UTF-8')
	f.write("")
	bot.send_message(message.chat.id, f"Отчистка завершена!")
	f.close()

def get_logs(message):
	current_dt = datetime.now().strftime("%d.%m.%y %H:%M:%S")
	c_date, c_time = current_dt.split()
	f = open('log.txt', 'a', encoding='UTF-8')
	f.write(f'{c_date} {c_time} - user: {message.from_user.first_name} @{message.from_user.username} - text: {message.text}.\n')
	f.close()

def weather(message):
	city = "Sochi"
	code_to_smile = {
        "Clear": "\U00002600",# Ясно
        "Clouds": "\U00002601",# Облачно
        "Rain": "\U00002614",# Дождь
        "Drizzle": "\U00002614",# Дождь
        "Thunderstorm": "\U000026A1",# Гроза
        "Snow": "\U0001F328",# Снег
        "Mist": "\U0001F32B"# Туман
    }
	try:
		get = requests.get(f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={open_weather_token}&units=metric&lang=ru")
		result_get = get.json()
		get_city = result_get['name']
		temp = str(result_get['main']['temp'])
		temp_max = str(result_get['main']['temp_max'])
		temp_min = str(result_get['main']['temp_min'])
		weather = str(result_get['weather'][0]['description'].capitalize())
		weather_description = result_get['weather'][0]['main']
		if weather_description in code_to_smile:
			weather_icon = code_to_smile[weather_description]
		else:
			weather_icon = ""
		# Комментарий от Гоши
		weather_status = "Без комментариев..."
		if weather_description == "Clear":
			weather_status = "Без очков не вариант выходить"
		if weather_description == "Clouds":
			weather_status = "Погода бомба, газуй гулять"
		if weather_description == "Rain":
			weather_status = "Дома сиди и кайфуй"
		if weather_description == "Drizzle":
			weather_status = "Дома сиди и кайфуй"
		if weather_description == "Thunderstorm":
			weather_status = "Больная погода! Даже в окно не смотри!"
		if weather_description == "Snow":
			weather_status = "Пора навести белую суету"
		if weather_description == "Mist":
			weather_status = "Чисто на кумаре. Балдеж..."
		sunrise = datetime.fromtimestamp(result_get['sys']['sunrise']).strftime("%H:%M")
		sunset = datetime.fromtimestamp(result_get['sys']['sunset']).strftime("%H:%M")
		bot.send_message(message.chat.id, f"🌅🌅🌅Погода в {get_city}🌅🌅🌅\n\n{weather} {weather_icon}\n\n🌡\nСейчас: {temp[:2]}°\nМинимум: {temp_min[:2]}°\nМаксимум: {temp_max[:2]}°\n\n☀️\nВосход: {sunrise}\nЗакат: {sunset}\n\nКомментарий от Гоши: {weather_status}")
	except:
		bot.send_message(message.chat.id, f"Странно.. Этого не должно было случиться")
		pass

def weekday_str(message):
	weekday = datetime.now().weekday()
	if weekday == 0:
		return "Понедельник"
	if weekday == 1:
		return "Вторник"
	if weekday == 2:
		return "Среда"
	if weekday == 3:
		return "Четверг"
	if weekday == 4:
		return "Пятница"
	if weekday == 5:
		return "Суббота"
	if weekday == 6:
		return "Воскресенье"

def payments(message):
	bot.send_message(message.chat.id, "Как приятно, что ты хочешь это сделать)\n\nЦелую твои руки😙")

@bot.message_handler(content_types=["text"])
def handle_text(message):
	banned = ["дурак", "мудак", "козел", "козёл", "черт", "чёрт", "гей", "хуй", "лох", "пидор"]
	chk_pat = '(?:{})'.format('|'.join(banned))
	try:
		if message.text:
			get_logs(message)					
		if message.text == "Узнать Гошу лучше":
			get_random_var_1(message)
		if message.text == "Загадки от Гоши":
			get_random_var_2(message)
		if message.text == "Узнать погоду у Гоши":
			weather(message)
		if message.text == "Забашлять Гоше":
			payments(message)
		if message.text == "Вернуться":
			start(message)
		# admin panel
		if message.text == "admin_panel":
			admin_panel(message)
		if message.text == "read_logs":
			read_logs(message)
		if message.text == "clear_logs":
			clear_logs(message)
		if message.text == "back_to_user":
			start(message)
		# check answer
		# 1.1
		if message.text == "Красный":
			bot.send_message(message.chat.id, "Пушка, гонка, автогонка 😍😍😍! Правильно!")
			variant_1_2(message)
		if message.text == "Зеленый":
			bot.send_message(message.chat.id, "Не правильно! Вася")
			variant_1_2(message)
		if message.text == "Черный":
			bot.send_message(message.chat.id, "Не правильно! Вася")
			variant_1_2(message)
		# 1.2
		if message.text == "Апельсиновый сок":
			bot.send_message(message.chat.id, "Пушка, гонка, автогонка 😍😍😍! Правильно!")
			variant_1_3(message)
		if message.text == "Coca-Cola":
			bot.send_message(message.chat.id, "Не правильно! Вася")
			variant_1_3(message)
		if message.text == "Черный чай":
			bot.send_message(message.chat.id, "Не правильно! Вася")
			variant_1_3(message)
		# 1.3
		if message.text == "Кушать":
			bot.send_message(message.chat.id, "Пушка, гонка, автогонка 😍😍😍! Правильно!")
			variant_1_4(message)
		if message.text == "Наяривать":
			bot.send_message(message.chat.id, "Не правильно! Вася")
			variant_1_4(message)
		if message.text == "Гулять":
			bot.send_message(message.chat.id, "Не правильно! Вася")
			variant_1_4(message)
		# 1.4
		if message.text == "Музыка":
			bot.send_message(message.chat.id, "Пушка, гонка, автогонка 😍😍😍! Правильно!")
			variant_1_5(message)
		if message.text == "Наука и техника":
			bot.send_message(message.chat.id, "Не правильно! Вася")
			variant_1_5(message)
		if message.text == "Видеоигры":
			bot.send_message(message.chat.id, "Не правильно! Вася")
			variant_1_5(message)
		# 1.5
		if message.text == "Лесби":
			bot.send_message(message.chat.id, "Пушка, гонка, автогонка 😍😍😍! Правильно!")
			variant_1_6(message)
		if message.text == "Гей":
			bot.send_message(message.chat.id, "Не правильно! Вася")
			variant_1_6(message)
		if message.text == "Классика":
			bot.send_message(message.chat.id, "Не правильно! Вася")
			variant_1_6(message)
		# 1.6
		if message.text == "M2":
			bot.send_message(message.chat.id, "Пушка, гонка, автогонка 😍😍😍! Правильно!")
			variant_1_1(message)
		if message.text == "M3":
			bot.send_message(message.chat.id, "Не правильно! Вася")
			variant_1_1(message)
		if message.text == "M5":
			bot.send_message(message.chat.id, "Не правильно! Вася")
			variant_1_1(message)
		# 2.1
		if message.text == "Славян":
			bot.send_message(message.chat.id, "Правильно!")
			variant_2_2(message)
		if message.text == "Чмо":
			bot.send_message(message.chat.id, "Тормоз!")
			variant_2_2(message)
		if message.text == "Цыпленок":
			bot.send_message(message.chat.id, "Тормоз!")
			variant_2_2(message)
		if message.text == "Персик":
			bot.send_message(message.chat.id, "Тормоз!")
			variant_2_2(message)
		# 2.2
		if message.text == "Ресторан":
			bot.send_message(message.chat.id, "Правильно!")
			variant_2_3(message)
		if message.text == "Авиакомпания":
			bot.send_message(message.chat.id, "Тормоз!")
			variant_2_3(message)
		if message.text == "Гошины приколы":
			bot.send_message(message.chat.id, "Тормоз!")
			variant_2_3(message)
		if message.text == "Тип, который сделал тебе больно":
			bot.send_message(message.chat.id, "Тормоз!")
			variant_2_3(message)
		# 2.3
		if message.text == "Армения":
			bot.send_message(message.chat.id, "Правильно!")
			variant_2_1(message)
		if message.text == "Россия":
			bot.send_message(message.chat.id, "Тормоз!")
			variant_2_1(message)
		if message.text == "Китай":
			bot.send_message(message.chat.id, "Тормоз!")
			variant_2_1(message)
		if message.text == "Америка":
			bot.send_message(message.chat.id, "Тормоз!")
			variant_2_1(message)
		# Проверка слов на запрет
		if re.search(chk_pat, message.text, flags=re.I):
			fun(message)
	except: 
		pass

def get_random_var_2(message):
	rand = random.randint(0, 2)
	if rand == 0:
		variant_2_1(message)
	if rand == 1:
		variant_2_2(message)
	if rand == 2:
		variant_2_3(message)

def variant_2_1(message):
	answer_1 = "Чмо"
	answer_2 = "Цыпленок"
	answer_3 = "Славян"
	answer_4 = "Персик"
	markups = types.ReplyKeyboardMarkup(row_width=2)
	btn_1 = types.KeyboardButton(f'{answer_1}')
	btn_2 = types.KeyboardButton(f'{answer_2}')
	btn_3 = types.KeyboardButton(f'{answer_3}')
	btn_4 = types.KeyboardButton(f'{answer_4}')
	btn_5 = types.KeyboardButton('Вернуться')
	markups.add(btn_1, btn_2, btn_3, btn_4, btn_5)
	bot.send_message(message.chat.id, f"Как называют молодого петуха?\n\n1. {answer_1}\n2. {answer_2}\n3. {answer_3}\n4. {answer_4}", reply_markup=markups)

def variant_2_2(message):
	answer_1 = "Ресторан"
	answer_2 = "Авиакомпания"
	answer_3 = "Гошины приколы"
	answer_4 = "Тип, который сделал тебе больно"
	markups = types.ReplyKeyboardMarkup(row_width=2)
	btn_1 = types.KeyboardButton(f'{answer_1}')
	btn_2 = types.KeyboardButton(f'{answer_2}')
	btn_3 = types.KeyboardButton(f'{answer_3}')
	btn_4 = types.KeyboardButton(f'{answer_4}')
	btn_5 = types.KeyboardButton('Вернуться')
	markups.add(btn_1, btn_2, btn_3, btn_4, btn_5)
	bot.send_message(message.chat.id, f"Что такое карабас?\n\n1. {answer_1}\n2. {answer_2}\n3. {answer_3}\n4. {answer_4}", reply_markup=markups)

def variant_2_3(message):
	answer_1 = "Россия"
	answer_2 = "Америка"
	answer_3 = "Китай"
	answer_4 = "Армения"
	markups = types.ReplyKeyboardMarkup(row_width=2)
	btn_1 = types.KeyboardButton(f'{answer_1}')
	btn_2 = types.KeyboardButton(f'{answer_2}')
	btn_3 = types.KeyboardButton(f'{answer_3}')
	btn_4 = types.KeyboardButton(f'{answer_4}')
	btn_5 = types.KeyboardButton('Вернуться')
	markups.add(btn_1, btn_2, btn_3, btn_4, btn_5)
	bot.send_message(message.chat.id, f"Скоро останется одна страна. Что это за страна?\n\n1. {answer_1}\n2. {answer_2}\n3. {answer_3}\n4. {answer_4}", reply_markup=markups)

def get_random_var_1(message):
	rand = random.randint(0, 5)
	if rand == 0:
		variant_1_1(message)
	if rand == 1:
		variant_1_2(message)
	if rand == 2:
		variant_1_3(message)
	if rand == 3:
		variant_1_4(message)
	if rand == 4:
		variant_1_5(message)
	if rand == 5:
		variant_1_6(message)

def variant_1_1(message):
	answer_1 = "Красный"
	answer_2 = "Зеленый"
	answer_3 = "Черный"
	markups = types.ReplyKeyboardMarkup(row_width=1)
	btn_1 = types.KeyboardButton(f'{answer_1}')
	btn_2 = types.KeyboardButton(f'{answer_2}')
	btn_3 = types.KeyboardButton(f'{answer_3}')
	btn_4 = types.KeyboardButton('Вернуться')
	markups.add(btn_1, btn_2, btn_3, btn_4)
	bot.send_message(message.chat.id, f"Вопрос №1\n{var_1[0]}\n\n1. {answer_1}\n2. {answer_2}\n3. {answer_3}", reply_markup=markups)

def variant_1_2(message):
	answer_1 = "Coca-Cola"
	answer_2 = "Черный чай"
	answer_3 = "Апельсиновый сок"
	markups = types.ReplyKeyboardMarkup(row_width=1)
	btn_1 = types.KeyboardButton(f'{answer_1}')
	btn_2 = types.KeyboardButton(f'{answer_2}')
	btn_3 = types.KeyboardButton(f'{answer_3}')
	btn_4 = types.KeyboardButton('Вернуться')
	markups.add(btn_1, btn_2, btn_3, btn_4)
	bot.send_message(message.chat.id, f"Вопрос №2\n{var_1[1]}\n\n1. {answer_1}\n2. {answer_2}\n3. {answer_3}", reply_markup=markups)

def variant_1_3(message):
	answer_1 = "Наяривать"
	answer_2 = "Кушать"
	answer_3 = "Гулять"
	markups = types.ReplyKeyboardMarkup(row_width=1)
	btn_1 = types.KeyboardButton(f'{answer_1}')
	btn_2 = types.KeyboardButton(f'{answer_2}')
	btn_3 = types.KeyboardButton(f'{answer_3}')
	btn_4 = types.KeyboardButton('Вернуться')
	markups.add(btn_1, btn_2, btn_3, btn_4)
	bot.send_message(message.chat.id, f"Вопрос №3\n{var_1[2]}\n\n1. {answer_1}\n2. {answer_2}\n3. {answer_3}", reply_markup=markups)

def variant_1_4(message):
	answer_1 = "Наука и техника"
	answer_2 = "Видеоигры"
	answer_3 = "Музыка"
	markups = types.ReplyKeyboardMarkup(row_width=1)
	btn_1 = types.KeyboardButton(f'{answer_1}')
	btn_2 = types.KeyboardButton(f'{answer_2}')
	btn_3 = types.KeyboardButton(f'{answer_3}')
	btn_4 = types.KeyboardButton('Вернуться')
	markups.add(btn_1, btn_2, btn_3, btn_4)
	bot.send_message(message.chat.id, f"Вопрос №4\n{var_1[3]}\n\n1. {answer_1}\n2. {answer_2}\n3. {answer_3}", reply_markup=markups)
		
def variant_1_5(message):
	answer_1 = "Лесби"
	answer_2 = "Гей"
	answer_3 = "Классика"
	markups = types.ReplyKeyboardMarkup(row_width=1)
	btn_1 = types.KeyboardButton(f'{answer_1}')
	btn_2 = types.KeyboardButton(f'{answer_2}')
	btn_3 = types.KeyboardButton(f'{answer_3}')
	btn_4 = types.KeyboardButton('Вернуться')
	markups.add(btn_1, btn_2, btn_3, btn_4)
	bot.send_message(message.chat.id, f"Вопрос №5\n{var_1[4]}\n\n1. {answer_1}\n2. {answer_2}\n3. {answer_3}", reply_markup=markups)

def variant_1_6(message):
	answer_1 = "M3"
	answer_2 = "M5"
	answer_3 = "M2"
	markups = types.ReplyKeyboardMarkup(row_width=1)
	btn_1 = types.KeyboardButton(f'{answer_1}')
	btn_2 = types.KeyboardButton(f'{answer_2}')
	btn_3 = types.KeyboardButton(f'{answer_3}')
	btn_4 = types.KeyboardButton('Вернуться')
	markups.add(btn_1, btn_2, btn_3, btn_4)
	bot.send_message(message.chat.id, f"Вопрос №6\n{var_1[5]}\n\n1. {answer_1}\n2. {answer_2}\n3. {answer_3}", reply_markup=markups)

def fun(message):
	bot.send_message(message.chat.id, "Это было зря...\n\n<b>Не трогай мобилу!!!</b>", parse_mode='html')
	time.sleep(2)
	bot.send_message(message.chat.id, "Беда случилась! Звони Гоше!\n\nУ тебя есть ровно 10 секунд!\nЭто не шутка! Поторопись!!!")
	time.sleep(2)
	bot.send_message(message.chat.id, "1")
	time.sleep(1)
	bot.send_message(message.chat.id, "2")
	time.sleep(1)
	bot.send_message(message.chat.id, "3")
	time.sleep(1)
	bot.send_message(message.chat.id, "4")
	time.sleep(1)
	bot.send_message(message.chat.id, "5")
	time.sleep(1)
	bot.send_message(message.chat.id, "6")
	time.sleep(1)
	bot.send_message(message.chat.id, "7")
	time.sleep(1)
	bot.send_message(message.chat.id, "8")
	time.sleep(1)
	bot.send_message(message.chat.id, "9")
	time.sleep(1)
	bot.send_message(message.chat.id, "10")
	time.sleep(1)
	bot.send_message(message.chat.id, "Мне очень жаль..")
	time.sleep(2)
	timer = 0
	while True:
		bot.send_message(message.chat.id, "<b>Уууу, суетаа...</b>", parse_mode='html')
		timer+=1
		if timer == 50:
			break
		

bot.polling(none_stop=True)
