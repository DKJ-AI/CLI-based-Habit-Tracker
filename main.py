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
    print("4. Delete habit")
    print("5. Exit")
    print()

    choice = input("Choose: ")

    data =load_data()

    if choice == "1":
      add_habit(data)
    elif choice == "2":
      view_habits(data)
    elif choice == "3":
      habit_name = input("Enter habit name to mark done: ").strip().title()
      mark_done(data, habit_name)
    elif choice == "4":
      habit_name = input("Enter habit name to delete: ").strip().title()
      delete_habit(data, habit_name)
    elif choice == "5":
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



def add_habit(data):
  new_habit = input("Enter habit name: ").strip().title()

  if new_habit in data:
    print(f"'{new_habit}' already exists.")
    return

  data[new_habit] = {"streak": 0, "last_done": None}
   
  save_data(data)
  print(f"Succesfully added {new_habit}")


def delete_habit(data, habit_name):
  if habit_name in data:
    del data[habit_name]

  save_data(data)
  print(f"Succesfully deleted {habit_name}")



def view_habits(data):
  print("\n--- HABITS ---")
  for habit, info in data.items():
    print(f"{habit}: Streak -> 🔥 {info['streak']} days | Last: {info['last_done']} ")
  if not data:
    print("No habits found.")
    return


def mark_done(data, habit):
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