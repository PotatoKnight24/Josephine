import os
import threading
import telebot
import requests
from flask import Flask
from dotenv import load_dotenv
from openai import OpenAI
from reciper_recommender import get_recipe
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton

load_dotenv()
bot = telebot.TeleBot(os.getenv("TELEGRAM_TOKEN"))
user_data = {}  # Store user responses

@bot.message_handler(commands=['start', 'hello'])
def send_welcome(message):
    bot.reply_to(message, "How can I help you today?")

@bot.message_handler(commands=['recommend'])
def get_meal_type(message):
    user_data[message.chat.id] = {}  # Initialize storage for user data
    
    # Create Inline Keyboard for Meal Type Selection
    markup = InlineKeyboardMarkup()
    buttons = [InlineKeyboardButton(text=meal, callback_data=f"meal_{meal}") for meal in ["Breakfast", "Lunch", "Dinner", "Snack"]]
    
    for btn in buttons:
        markup.add(btn)

    bot.send_message(message.chat.id, "What kind of meal do you want?", reply_markup=markup)

# Handle Meal Type Selection
@bot.callback_query_handler(func=lambda call: call.data.startswith("meal_"))
def handle_meal_type(call):
    meal_type = call.data.split("_")[1]  # Extract the meal type from callback data
    user_data[call.message.chat.id]['type'] = meal_type
    bot.send_message(call.message.chat.id, "How much time do you have? (in minutes)")
    bot.register_next_step_handler(call.message, get_fanciness)

# Handle User Input for Duration
def get_fanciness(message):
    user_data[message.chat.id]['duration'] = message.text  # Store duration

    # Create Inline Keyboard for Fanciness Selection (1-10)
    markup = InlineKeyboardMarkup()
    buttons = [InlineKeyboardButton(text=str(i), callback_data=f"fanciness_{i}") for i in range(1, 11)]
    
    # Display buttons in rows of 5
    for i in range(0, 10, 5):
        markup.row(*buttons[i:i+5])

    bot.send_message(message.chat.id, "How fancy do you want it to be? (1-10)", reply_markup=markup)

# Handle Fanciness Selection
@bot.callback_query_handler(func=lambda call: call.data.startswith("fanciness_"))
def handle_fanciness(call):
    fanciness_level = call.data.split("_")[1]  # Extract fanciness level
    user_data[call.message.chat.id]['fanciness'] = fanciness_level
    bot.send_message(call.message.chat.id, "Any other preferences?")
    bot.register_next_step_handler(call.message, process_meal)

# Handle Additional Notes & Process Recipe Request
def process_meal(message):
    user_data[message.chat.id]['other_notes'] = message.text  # Store other notes

    # Retrieve stored data
    prompt_args = user_data[message.chat.id]
    
    # Get the recommended recipe
    reply = get_recipe(
        prompt_args['type'], 
        prompt_args['duration'], 
        prompt_args['fanciness'], 
        prompt_args['other_notes']
    )

    bot.reply_to(message, f"Here is your meal recommendation:\n{reply}")
app = Flask(__name__)

@app.route('/')
def home():
    return "Bot is running!"

def run_flask():
    app.run(host='0.0.0.0', port=int(os.getenv("PORT", 10000)),debug = False)

# Start Flask in a separate thread
server = threading.Thread(target=run_flask)
server.start()

# Start Telegram bot

bot.polling(non_stop=True, skip_pending=True)

