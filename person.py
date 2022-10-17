import telebot
from telebot import types
import random
import psycopg2
from dotenv import load_dotenv
from pathlib import Path
import os

load_dotenv()
env_path = Path('.')/'.env'
load_dotenv(dotenv_path=env_path)

token = os.getenv('TOKEN')

bot = telebot.TeleBot(token)
conn = psycopg2.connect(host="159.223.20.145", dbname="server", user="server", password="codabra")
db = conn.cursor()

@bot.message_handler(content_types=['text'])
def idle(message):
    if message.text == '/start' and checkuser(message.from_user.id) == False:
        bot.send_message(message.from_user.id, "Добро пожаловать в игру, назови своего персонажа.")
        bot.register_next_step_handler(message, givename)
    if message.text == '/test':
        getstats(message.from_user.id)
    if message.text == '/test2':
        getenemyes(message.from_user.id)




def givename(message):
    name = message.text
    db.execute("INSERT INTO persona (user_id, name) VALUES (%s, %s)", (message.from_user.id, name))
    conn.commit()
    bot.send_message(message.from_user.id, "Привет " + name + ". Добро пожаловать в мир, для продолжения напиши команду /game.")

def checkuser(id):
    db.execute("SELECT * FROM persona WHERE user_id = %s", (id,))
    if db.fetchone() is None:
        return False
    else:
        return True

# 0 - id
# 1 - hp
# 2 - energy
# 3 - attack
# 4 - defend
# 5 - villagers
# 6 - stels
# 7 - name

def getstats(id):
    db.execute("SELECT * FROM persona WHERE user_id = %s", (id,))
    answer = db.fetchone()

    bot.send_message(id,
f"""
Привет {answer[7]}, вот твоя статистика:
Здоровье - {answer[1]}
Энергия - {answer[2]}
Урон - {answer[3]}
Защита - {answer[4]}
Жители - {answer[5]}
Скрытность - {answer[6]}
""")

# 0 - id
# 1 - hp
# 2 - damage
# 3 - defend
# 4 - visibility
# 5 - name

def getenemyes(id):
    db.execute("SELECT * FROM enemy")
    answer = db.fetchall()
    text = 'Вот информация о всех противниках:'

    for enemy in answer:
        text += f"""
---
Имя - {enemy[5]} / Здоровье - {enemy[1]} / Урон - {enemy[2]} / Защита - {enemy[3]} / Зоркость - {enemy[4]}
---
"""

    bot.send_message(id, text)


bot.polling(none_stop=True, interval=0)

