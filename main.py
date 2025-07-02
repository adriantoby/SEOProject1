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

experience = -1
while experience not in ["beginner", "intermediate", "expert"]:
    try:
        experience = int(input("How many years of experience do you have?\n"))
    except:
        print("\nPlease enter a valid number of years.")
        continue

    if experience == 0 or experience == 1:
        experience = "beginner"
    elif experience > 1 and experience <= 4:
        experience = "intermediate"
    elif experience > 4:
        experience = "expert"
    else:
        print("\nPlease enter a valid number of years.")

print()
goal = -1
while goal not in ["endurance", "strength", "bodybuilding"]:
    try:
        goal = int(input("What is your workout goal? (1-Endurance, 2-Strength, 3-Bodybuilding)\n"))
    except:
        print("\nPlease enter a valid option.")
        continue

    if goal == 1:
        goal = "endurance"
        workout_type = "cardio"
    elif goal == 2:
        goal = "strength"
        workout_type = "powerlifting"
    elif goal == 3:
        goal = "bodybuilding"
        workout_type = "strength"
    else:
        print("\nPlease enter a valid option.")


print()
diet_type = -1
while diet_type not in ["vegetarian", "low-carb", "high-protein"]:
    try:
        diet_type = int(input("What diet do you prefer? (1-Vegetarian, 2-Low Carb, 3-High Protein)\n"))
    except:
        print("\nPlease enter a valid option.")
        continue

    if diet_type == 1:
        diet_type = "vegetarian"
        food_base_url_extension = "complexSearch?diet=vegetarian"
    elif diet_type == 2:
        diet_type = "low-carb"
        food_base_url_extension = "findByNutrients?minCarbs=15&maxCarbs=35"
    elif diet_type == 3:
        diet_type = "high-protein"
        food_base_url_extension = "findByNutrients?minProtein=45"
    else:
        print("\nPlease enter a valid option.")

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
# exercise_response = requests.get(exercise_base_url + f"?difficulty={experience}&type={workout_type}", headers=exercise_headers)
# exercises = exercise_response.json()

food_response = requests.get(food_base_url + food_base_url_extension, headers=food_headers)
foods = food_response.json()
if diet_type == "vegetarian":
    foods = foods["results"]

# print(foods)


food_df = pd.DataFrame.from_dict(foods)

engine = db.create_engine('sqlite:///health.db')

# df.to_sql('exercises', con=engine, if_exists='replace', index=False)
food_df.to_sql('foods', con=engine, if_exists='replace', index=False)

with engine.connect() as connection:
   query_result = connection.execute(db.text("SELECT * FROM foods;")).fetchall()
#    print(pd.DataFrame(query_result))


my_api_key = os.getenv('GENAI_API_KEY')

# genai.api_key = my_api_key

# Create an genAI client using the key from our environment variable
client = genai.Client(
    api_key=my_api_key,
)

# Specify the model to use and the messages to send
response = client.models.generate_content(
    model="gemini-2.5-flash",
    config=types.GenerateContentConfig(
      system_instruction="You are a professional fitness and nutrition coach who knows how to make the most optimal fitness and nutrition plans for a user based on their experience and preferences."
    ),
    contents=f"Look through {pd.DataFrame(query_result)} and create a nutrition plan for {experience}s who want to focus on {goal} with a {diet_type}-focused diet. Keep the nutrition plan optimal, and explain your reasoning in a concise manner.",
)

# Look through {pd.DataFrame(query_result)} and create a workout routine for {experience}s who want to focus on {goal}. Keep the workout plan optimal, and explain your reasoning in a concise manner.

print(response.text)
print()
print("Enjoy your workout and nutrition plan!")