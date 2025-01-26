from dotenv import load_dotenv
import os
import telebot

# Explicitly load the .env file from the current directory
load_dotenv(dotenv_path="./.env")

# Get the BOT_TOKEN from the .env file
BOT_TOKEN = os.getenv('BOT_TOKEN')

# Ensure that the BOT_TOKEN is found
if not BOT_TOKEN:
    raise ValueError("BOT_TOKEN not found! Make sure it's set in the .env file.")

# Initialize the TeleBot with the correct BOT_TOKEN
bot = telebot.TeleBot(BOT_TOKEN)

@bot.message_handler(commands=['start', 'hello'])
def send_welcome(message):
    bot.reply_to(message, "Howdy, how are you doing?")

@bot.message_handler(func=lambda msg: True)
def echo_all(message):
    bot.reply_to(message, message.text)

bot.infinity_polling()
