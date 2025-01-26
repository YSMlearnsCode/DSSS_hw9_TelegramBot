import os
from dotenv import load_dotenv
import telebot
import torch
from transformers import pipeline

# Load the .env file
load_dotenv(dotenv_path="./.env")

# Get the BOT_TOKEN from the .env file
BOT_TOKEN = os.getenv('BOT_TOKEN')

# Ensure the BOT_TOKEN is found
if not BOT_TOKEN:
    raise ValueError("BOT_TOKEN not found! Make sure it's set in the .env file.")

# Initialize the Telegram bot
bot = telebot.TeleBot(BOT_TOKEN)

# Load TinyLlama model using Hugging Face's pipeline
pipe = pipeline("text-generation", model="TinyLlama/TinyLlama-1.1B-Chat-v1.0", 
                torch_dtype=torch.bfloat16, device_map="auto")

# Function to handle incoming messages
@bot.message_handler(commands=['start', 'hello'])
def send_welcome(message):
    bot.reply_to(message, "Howdy! I am your AI assistant powered by TinyLlama. Ask me anything!")

@bot.message_handler(func=lambda msg: True)
def respond_to_message(message):
    # Format the message for TinyLlama
    user_message = message.text
    print(f"User Message: {user_message}")
    
    # Use the tokenizer's chat template to format the message
    messages = [
        {"role": "system", "content": "You are a friendly chatbot who always responds in the style of a pirate."},
        {"role": "user", "content": user_message},
    ]
    prompt = pipe.tokenizer.apply_chat_template(messages, tokenize=False, add_generation_prompt=True)

    # Generate a response using the TinyLlama model
    outputs = pipe(prompt, max_new_tokens=256, do_sample=True, temperature=0.7, top_k=50, top_p=0.95)
    response = outputs[0]["generated_text"]
    
    # Send the model's response to the user
    bot.reply_to(message, response)

# Start the bot's polling loop to listen for messages
bot.infinity_polling()
