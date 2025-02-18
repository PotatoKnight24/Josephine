import openai
import config
from dotenv import load_dotenv
from google_sheets import get_food_list
load_dotenv()
client = openai.OpenAI(api_key=config.OPEN_API_KEY)
def get_recipe(meal_type,duration,difficulty,other_notes = ''):
    prompt = f"""
    You are a home-cooking recipe assistant. Recommend a recipe for a {meal_type} 
    that takes at most {duration} minutes to prepare and is {difficulty} difficulty. 
    additional requirements are as follows {other_notes}. 
    The following list contains the ingredients available in the users house please try as much as possible use
    ingredients in this list:
    {get_food_list()}
    Focus on ease of obtaining ingredients unless otherwise stated, user is a workfrom home office worker who is trying to eat healthy
    
    Ensure the response follows this exact format:
    please ensure that you use {meal_type} {duration} {difficulty} as specified, do not come up with your own
    🍽 *Recipe Name:* [Generated Name]
    🕒 *Time Required:* [as specified]
    🔥 *Fanciness:* [as specified]
    🥣 **Ingredients:** 
       - Ingredient 1
       - Ingredient 2
       - Ingredient 3
       
    👨‍🍳 *Instructions:*
    1. Step 1
    2. Step 2
    3. Step 3
    

    """
    
    # try:
    response = client.chat.completions.create(
    model = "gpt-4o",
    messages = [{
        "role" : "user",
        "content" : prompt
    }])
    recipe = response.choices[0].message.content
    # except openai.APIError as e:
    #     return "Sorry, I couldn't fetch a recipe at the moment. Please try later!"
    # except Exception as e:
    #     return "Something went wrong... Try again later!"


    return recipe
