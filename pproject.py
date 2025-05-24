import xml.etree.ElementTree as ET
import csv
import matplotlib.pyplot as plt

workout_categories = ['Cardio', 'Strength', 'Yoga', 'Pilates']
meal_categories = ['Breakfast', 'Lunch', 'Dinner', 'Snack']

user_profiles = {}

def input_entry():
    entry_type = input("Enter the type of entry (Workout/Meal): ").capitalize()

    if entry_type not in ['Workout', 'Meal']:
        print("Invalid entry type!")
        return None

    if entry_type == 'Workout':
        category = input(f"Choose a workout category from {workout_categories} or enter a new one: ")
        if category not in workout_categories:
            workout_categories.append(category)
    elif entry_type == 'Meal':
        category = input(f"Choose a meal category from {meal_categories} or enter a new one: ")
        if category not in meal_categories:
            meal_categories.append(category)

    if entry_type == 'Workout':
        duration = input("Enter the duration of the workout (e.g., 30 minutes): ")
    else:
        duration = input("Enter the quantity of the meal (e.g., 1 plate): ")

    calories = input("Enter the calories (number only): ")
    try:
        calories = int(calories)
    except ValueError:
        print("Invalid input for calories.")
        return None

    date = input("Enter the date (YYYY-MM-DD): ")

    entry = {
        'type': entry_type,
        'category': category,
        'duration_quantity': duration,
        'calories': calories,
        'date': date
    }

    return entry

def create_user_profile():
    username = input("Enter your username: ")
    if username not in user_profiles:
        user_profiles[username] = {
            'stats': {'weight': None, 'height': None, 'fitness_goal': None},
            'entries': []
        }
        print(f"Profile for {username} created!")
    else:
        print(f"Welcome back, {username}!")
    return username

def edit_profile(username):
    print("\n--- Edit Your Profile Information ---")
    weight = input("Enter your weight (kg): ")
    height = input("Enter your height (cm): ")
    goal = input("Enter your fitness goal (e.g., Lose weight, Gain muscle): ")

    user_profiles[username]['stats']['weight'] = weight
    user_profiles[username]['stats']['height'] = height
    user_profiles[username]['stats']['fitness_goal'] = goal
    print("Profile updated successfully!")

def import_from_csv(filename, username):
    try:
        with open(filename, 'r') as file:
            reader = csv.DictReader(file)
            for row in reader:
                entry = {
                    'type': row['type'],
                    'category': row['category'],
                    'duration_quantity': row['duration_quantity'],
                    'calories': int(row['calories']),
                    'date': row['date']
                }
                user_profiles[username]['entries'].append(entry)
        print(f"Data imported successfully for {username}")
    except FileNotFoundError:
        print(f"File {filename} not found!")

def import_from_xml(filename, username):
    try:
        tree = ET.parse(filename)
        root = tree.getroot()

        for entry in root.findall('entry'):
            entry_data = {
                'type': entry.find('type').text,
                'category': entry.find('category').text,
                'duration_quantity': entry.find('duration_quantity').text,
                'calories': int(entry.find('calories').text),
                'date': entry.find('date').text
            }
            user_profiles[username]['entries'].append(entry_data)
        print(f"Data imported successfully for {username} from XML.")
    except FileNotFoundError:
        print(f"File {filename} not found!")
    except ET.ParseError:
        print(f"Error parsing the XML file {filename}. Please check the format.")

def visualize_data(username):
    # Calories burned vs. consumed
    workout_calories = sum(entry['calories'] for entry in user_profiles[username]['entries'] if entry['type'] == 'Workout')
    meal_calories = sum(entry['calories'] for entry in user_profiles[username]['entries'] if entry['type'] == 'Meal')

    labels = ['Calories Burned', 'Calories Consumed']
    values = [workout_calories, meal_calories]

    # Bar chart for calories
    plt.bar(labels, values, color=['blue', 'orange'])
    plt.xlabel('Calories')
    plt.ylabel('Amount')
    plt.title(f'Calories Burned vs. Consumed for {username}')
    plt.show()

    # Meal category distribution
    meal_counts = {}
    for entry in user_profiles[username]['entries']:
        if entry['type'] == 'Meal':
            meal_counts[entry['category']] = meal_counts.get(entry['category'], 0) + 1

    if meal_counts:
        plt.bar(meal_counts.keys(), meal_counts.values(), color='green')
        plt.xlabel('Meal Categories')
        plt.ylabel('Frequency')
        plt.title(f'Meal Categories Distribution for {username}')
        plt.show()

def main():
    username = create_user_profile()

    edit_profile(username)

    import_xml = input("Do you want to import data from an XML file? (yes/no): ").lower()
    if import_xml == 'yes':
        filename = input("Enter the XML filename: ")
        import_from_xml(filename, username)

    while True:
        entry = input_entry()
        if entry:
            user_profiles[username]['entries'].append(entry)
            print(f"Entry added for {username}: {entry}")
        else:
            print("Entry not added due to invalid input.")

        more_entries = input("Do you want to add another entry? (yes/no): ").lower()
        if more_entries != 'yes':
            break

    print(f"\nAll entries for {username}:")
    for entry in user_profiles[username]['entries']:
        print(entry)

    visualize = input("Do you want to visualize the data? (yes/no): ").lower()
    if visualize == 'yes':
        visualize_data(username)

    # End message
    print("\nProgram finished. Thank you for using the Fitness and Nutrition Tracker!")

if __name__ == "__main__":
    main()
aanpo