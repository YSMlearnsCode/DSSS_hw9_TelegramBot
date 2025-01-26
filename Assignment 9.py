from dotenv import load_dotenv
import os
import telebot
from transformers import pipeline  # Import LLM (e.g., TinyLlama, GPT, etc.)

# Load environment variables from .env file
load_dotenv(dotenv_path="./.env")

# Get the BOT_TOKEN from the .env file
BOT_TOKEN = os.getenv('BOT_TOKEN')

# Ensure that the BOT_TOKEN is found
if not BOT_TOKEN:
    raise ValueError("BOT_TOKEN not found! Make sure it's set in the .env file.")

# Initialize the TeleBot with the correct BOT_TOKEN
bot = telebot.TeleBot(BOT_TOKEN)

#Delete if needed
import os
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '2'  # Suppresses TensorFlow info and warnings





# Load the AI model (using a simple Huggingface model or TinyLlama if you prefer)
# You can replace this with the TinyLlama model (or similar LLM) depending on your setup
llm_model = pipeline('text-generation', model='gpt2')  # Replace 'gpt2' with your local model

def get_ai_response(user_input):
    # Generate the AI's response based on the user input
    ai_response = llm_model(user_input, max_length=100)[0]['generated_text']
    return ai_response

@bot.message_handler(commands=['start', 'hello'])
def send_welcome(message):
    bot.reply_to(message, "Howdy! How can I assist you today? Ask me anything!")

@bot.message_handler(func=lambda msg: True)
def handle_message(message):
    # Capture the message sent by the user
    user_input = message.text
    ai_response = get_ai_response(user_input)  # Get AI response

    # Send the response back to the user
    bot.reply_to(message, ai_response)

# Start polling for messages
bot.infinity_polling()
