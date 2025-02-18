import os
import telebot
import requests
from dotenv import load_dotenv
from openai import OpenAI
from reciper_recommender import get_recipe
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton

load_dotenv()
bot = telebot.TeleBot(os.getenv("TELEGRAM_TOKEN"))

# Global storage for user session
meal_type = None
duration = None
fanciness = None

@bot.message_handler(commands=['start', 'hello'])
def send_welcome(message):
    bot.reply_to(message, "How can I help you today? \n/recommend ")

@bot.message_handler(commands=['recommend'])
def get_meal_type(message):
    global meal_type, duration, fanciness
    meal_type = duration = fanciness = None  # Reset session data
    
    # Create Inline Keyboard for Meal Type Selection
    markup = InlineKeyboardMarkup()
    buttons = [InlineKeyboardButton(text=meal, callback_data=f"meal_{meal}") for meal in ["Breakfast", "Lunch", "Dinner", "Snack"]]
    
    for btn in buttons:
        markup.add(btn)

    bot.send_message(message.chat.id, "What kind of meal do you want?", reply_markup=markup)

# Handle Meal Type Selection
@bot.callback_query_handler(func=lambda call: call.data.startswith("meal_"))
def handle_meal_type(call):
    global meal_type
    meal_type = call.data.split("_")[1]  # Store meal type
    bot.send_message(call.message.chat.id, "How much time do you have? (in minutes)")
    bot.register_next_step_handler(call.message, get_fanciness)

# Handle User Input for Duration
def get_fanciness(message):
    global duration
    duration = message.text  # Store duration

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
    global fanciness
    fanciness = call.data.split("_")[1]  # Store fanciness level
    bot.send_message(call.message.chat.id, "Any other preferences?")
    bot.register_next_step_handler(call.message, process_meal)

# Handle Additional Notes & Process Recipe Request
def process_meal(message):
    global meal_type, duration, fanciness

    other_notes = message.text  # Store additional notes

    # Get the recommended recipe
    reply = get_recipe(meal_type, duration, fanciness, other_notes)

    bot.reply_to(message, f"Here is your meal recommendation:\n{reply}")

    # Reset variables after processing
    meal_type = duration = fanciness = None


bot.polling()
