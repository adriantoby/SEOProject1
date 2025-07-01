import requests
import pandas as pd
import sqlalchemy as db
import os 
from google import genai
from google.genai import types
from dotenv import load_dotenv

'''

Idea:
    Ask user questions:
        Exercise goal (strength training, endurance, …)
        Experience level
        Meal plan type (low carb, high protein, keto, …)
        
    Print workout plan and nutrition plan


APIS: 
    Workouts api: https://www.api-ninjas.com/api/exercises
    Recipes api:https://spoonacular.com/food-api/apps
    https://spoonacular.com/food-api/docs


BONUS:
	Access to gym 
	Filter by equipment type
    Food allergies


WORKFLOW:
    introduce the program -> print statement of what the project is
    ask user questions
        strength(1), endurance(2)
        meal plan stuff
    set up authentication for APIS
    get JSONs from APIs
    create database with JSON information
    parse inputs into specific AI queries
    display results in clean format
    bonus features if time

'''

print("Welcome to the Fitness and Nutrition Planner!\n")


experience = int(input("How many years of experience do you have?\n"))
if experience <= 1:
    experience = "beginner"
elif experience <= 4:
    experience = "intermediate"
else:
    experience = "expert"

goal = int(input("What is your workout goal? (1-Endurance, 2-Strength, 3-Bodybuilding)\n"))
if goal == 1:
    workout_type = "cardio"
elif goal == 2:
    workout_type = "powerlifting"
else:
    workout_type = "strength"


print()
diet_type = int(input("What diet do you prefer? (1-Vegetarian, 2-Low Carb, 3-High Protein)\n"))
if diet_type == 1:
    pass
elif diet_type == 2:
    pass
else:
    pass

print()
print("Generating program...\n")

# get access tokens and sign into APIS

load_dotenv()
exercise_api_key = os.getenv("EXERCISE_API_KEY")
food_api_key = os.getenv("FOOD_API_KEY")

exercise_headers = {
    'X-Api-Key': exercise_api_key
}


food_headers = {
    "x-api-key": food_api_key
}

exercise_base_url = "https://api.api-ninjas.com/v1/exercises"
food_base_url = "https://api.spoonacular.com/recipes/"

# do GET requests
# response = requests.get(exercise_base_url + f"?difficulty={experience}&type={workout_type}", headers=exercise_headers)
response = requests.get(food_base_url + "findByNutrients?minProtein=35", headers=food_headers)
# print(response.json())


df = pd.DataFrame.from_dict(response.json())

engine = db.create_engine('sqlite:///health.db')

# df.to_sql('exercises', con=engine, if_exists='replace', index=False)
df.to_sql('foods', con=engine, if_exists='replace', index=False)

with engine.connect() as connection:
   query_result = connection.execute(db.text("SELECT * FROM foods;")).fetchall()
   print(pd.DataFrame(query_result))


my_api_key = os.getenv('GENAI_API_KEY')

# genai.api_key = my_api_key

# Create an genAI client using the key from our environment variable
client = genai.Client(
    api_key=my_api_key,
)

# Specify the model to use and the messages to send
# response = client.models.generate_content(
#     model="gemini-2.5-flash",
#     config=types.GenerateContentConfig(
#       system_instruction="You are a professional fitness and nutrition coach who knows how to make the most optimal fitness and nutrition plans for a user based on their experience and preferences."
#     ),
#     contents=f"Look through {pd.DataFrame(query_result)} and create a workout routine for {experience}s who want to focus on {goal}. Keep the workout plan optimal, and explain your reasoning in a concise manner.",
# )


# print(response.text)


print("Enjoy your workout and nutrition plan!")