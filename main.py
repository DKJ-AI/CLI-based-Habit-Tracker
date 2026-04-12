import json
import os
from datetime import datetime, timedelta



def main():
  data = load_data()

  while True:

    print() 
    print("1. Add Habit")
    print("2. View Habits")
    print("3. Mark Done")
    print("4. Exit")
    print()

    choice = input("Choose: ")

    if choice == "1":
      add_habit_to_json()
    elif choice == "2":
      view_habits()
    elif choice == "3":
      mark_done()
    elif choice == "4":
      break
    else:
      print("Invalid choice")
  


def load_data():
  filename = 'habit.json'

  if not os.path.exists(filename):
    return {}
  with open(filename,'r') as json_file:
    try:
      data = json.load(json_file)
      return data if isinstance(data, dict) else {}
    except json.JSONDecodeError:
      return {}



def save_data(data):
   with open('habit.json', 'w') as json_file:
    json.dump(data, json_file, indent=4)



def add_habit_to_json():
  data = load_data()

  new_habit = input("Enter habit name: ").strip().capitalize()

  if new_habit in data:
    print(f"'{new_habit}' already exists.")
    return

  data[new_habit] = {"streak": 0, "last_done": None}
   
  save_data(data)
  print(f"Succesfully added {new_habit}")



def view_habits():
  data = load_data()
  print("\n--- HABITS ---")
  for habit, info in data.items():
    print(f"{habit}: Streak -> {info['streak']} days (Last done : {info['last_done']}) ")



def mark_done():
  data = load_data()

  habit = input("Enter habit name to mark done: ").strip().capitalize()
  
  if habit not in data:
    print("Habit not found")
    return
  
  today = datetime.today().date()
  last_done_str = data[habit]["last_done"]

  if last_done_str:
    last_done = datetime.strptime(last_done_str,"%Y-%m-%d").date()

    if last_done == today:
      print("Already marked done today!")
      return
    elif last_done == today-timedelta(days=1):
      data[habit]['streak'] += 1
    else:
      data[habit]['streak'] = 1

  else:
    data[habit]['streak'] = 1


  data[habit]["last_done"] = str(today)
  save_data(data)
  print(f"'{habit}' marked done! 🔥 Streak: {data[habit]['streak']} days")
   


if __name__ == "__main__":
    main()