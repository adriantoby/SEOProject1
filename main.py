import requests
import pandas as pd
import sqlalchemy as db
import os
from google import genai
from google.genai import types
from dotenv import load_dotenv
import parser


# collect user inputs
print("Welcome to NutriFit: Your Convenient Fitness and Nutrition Planner!\n")

experience = parser.years_of_experience()
goal, workout_type = parser.workout_info()
diet_type, food_base_url_extension = parser.diet()

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


# do GET requests
exercise_base_url = "https://api.api-ninjas.com/v1/exercises"
food_base_url = "https://api.spoonacular.com/recipes/"

exercise_base_url_extension = f"?difficulty={experience}&type={workout_type}"
exercise_response = requests.get(exercise_base_url +
                                 exercise_base_url_extension,
                                 headers=exercise_headers)
exercises = exercise_response.json()

food_response = requests.get(food_base_url + food_base_url_extension,
                             headers=food_headers)
foods = food_response.json()
if diet_type == "vegetarian":
    foods = foods["results"]

# print(exercises)
# print(foods)


# create and query database
exercise_df = pd.DataFrame.from_dict(exercises)
food_df = pd.DataFrame.from_dict(foods)

engine = db.create_engine('sqlite:///health.db')

exercise_df.to_sql('exercises', con=engine, if_exists='append', index=False)
food_df.to_sql('foods', con=engine, if_exists='append', index=False)

with engine.connect() as connection:
    exercise_query_result = connection.execute(
        db.text("SELECT * FROM exercises;")).fetchall()
    food_query_result = connection.execute(
        db.text("SELECT * FROM foods;")).fetchall()
#    print(pd.DataFrame(query_result))


# create and use GenAI API
my_api_key = os.getenv('GENAI_API_KEY')

client = genai.Client(
    api_key=my_api_key,
)

response = client.models.generate_content(
    model="gemini-2.5-flash",
    config=types.GenerateContentConfig(
        system_instruction="""You are a professional fitness and nutrition
        coach who knows most optimal fitness and nutrition plans for a user
        based on their background. You provide clear and concise plans and
        explanations with the most valuable information possible. You
        provide easy-to-read responses with no markdown syntax."""),
    contents=f"""Look through {exercise_query_result} and
    {food_query_result} to create a workout and nutrition plan for
    {experience}s who want to focus on {goal} with a {diet_type}-focused
    diet. Keep both plans optimal and explained-well yet concise. Do not
    include IDs of the recipes in your answer.""",
)

print(response.text)
print()
print("Enjoy your NutriFit workout and nutrition plan!")
