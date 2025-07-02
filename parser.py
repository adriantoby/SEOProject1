def years_of_experience():
    experience = -1
    text = "How many years have you been exercising?\n"
    while experience not in ["beginner", "intermediate", "expert"]:
        try:
            experience = int(input(text))
        except ValueError:
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

    return experience


def workout_info():
    print()
    goal = -1
    text = "What is your goal? (1-Endurance, 2-Strength, 3-Bodybuilding)\n"
    while goal not in ["endurance", "strength", "bodybuilding"]:
        try:
            goal = int(input(text))
        except ValueError:
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

    return goal, workout_type


def diet():
    print()
    diet_type = -1
    t = "What diet do you prefer? (1-Vegetarian, 2-Low Carb, 3-High Protein)\n"
    while diet_type not in ["vegetarian", "low-carb", "high-protein"]:
        try:
            diet_type = int(input(t))
        except ValueError:
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

    return diet_type, food_base_url_extension
