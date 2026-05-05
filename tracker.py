import json
import os
from datetime import datetime, timedelta

class HabitTracker:
    
    def __init__(self):
      self.filename = 'habit.json'  # the database of this project
      self.data = self.load_data()

    def load_data(self):
      filename = self.filename

      if not os.path.exists(filename):
        return {}
      with open(filename,'r') as json_file:
        try:
          data = json.load(json_file)
          return data if isinstance(data, dict) else {}
        except json.JSONDecodeError:
          return {}   
        

    def save_data(self): 
      with open(self.filename, 'w') as json_file:
        json.dump(self.data, json_file, indent=4)


    def select_habit(self):    # this will help to reduce human input error
      habits = list(self.data.keys())

      if not habits:
        print("No habits found.")
        return None
      
      print("\nSelect a habit:")
      print()
      for i, habit in enumerate(habits, 1):
        print(f"{i}. {habit}")

      try:
        choice = int(input("Enter number: "))
        if 1 <= choice <= len(habits):
            return habits[choice - 1]
        else:
            print("Invalid number")
            return None
      except ValueError:
        print("Enter a valid number")
        return None


    def add_habit(self): 
      new_habit = input("Enter habit name: ").strip().title()

      if new_habit in self.data:
        print(f"'{new_habit}' already exists.")
        return
      
      self.data[new_habit] = {"streak": 0, "last_done": None}
      self.save_data()
      print(f"Succesfully added '{new_habit}'")


    def delete_habit(self, habit_name):
      if habit_name in self.data:
        del self.data[habit_name]
        print(f"Succesfully deleted '{habit_name}'")
      else:
        print(f"Habit '{habit_name}' not found")

      self.save_data()


    def view_habits(self):
      if not self.data:
        print("No habits found.")
        return
      for habit, info in self.data.items():
        print(f"{habit}: Streak -> 🔥 {info['streak']} days | Last: {info['last_done']} ")
      

    def mark_done(self, habit):
      if habit not in self.data:
        print(f"'{habit}' not found")
        return
      
      today = datetime.today().date()
      last_done_str = self.data[habit]["last_done"]

      if last_done_str:
        last_done = datetime.strptime(last_done_str,"%Y-%m-%d").date()

        if last_done == today:
          print("Already marked done today!")
          return
        elif last_done == today-timedelta(days=1):
          self.data[habit]['streak'] += 1
        else:
          self.data[habit]['streak'] = 1
          self.data[habit]['last_done'] = str(today)
          print("Streak broken")
          print(f"'{habit}' 's Streak resetted to {self.data[habit]['streak']} days")
          self.save_data()
          return

      else:
        self.data[habit]['streak'] = 1


      self.data[habit]["last_done"] = str(today)
      self.save_data()
      print(f"'{habit}' marked done! 🔥 Streak: {self.data[habit]['streak']} days")


    def weekly_report(self):
      if not self.data:
        print(f"No habit found")
        return
      
      today = datetime.today().date()
      for habit, info in self.data.items():
        last_done_str = info["last_done"]

        if last_done_str:
          last_done = datetime.strptime(last_done_str,"%Y-%m-%d").date()

          status = "✅ Active" if last_done >= today-timedelta(days=7) else "❌ Inactive"
          
        else:
          status = "❌ Inactive"
        
        print(f"{habit}: Streak -> 🔥 {info['streak']} days | Status: {status} ")



def main():
  tracker = HabitTracker()

  while True:
    print() 
    print("1. Add Habit")
    print("2. View Habits & Streak")
    print("3. Mark Done")
    print("4. Delete habit")
    print("5. Weekly Report")
    print("6. Exit")
    print()

    choice = input("Choose: ").strip()

    if choice == "1":
      tracker.add_habit()
    elif choice == "2":
      tracker.view_habits()
    elif choice == "3":
      habit_name = tracker.select_habit()
      if habit_name:
        tracker.mark_done(habit_name)
    elif choice == "4":
      habit_name = tracker.select_habit()
      if habit_name:
        tracker.delete_habit(habit_name)
    elif choice == "5":
      tracker.weekly_report()
    elif choice == "6":
      break
    else:
      print("Invalid choice")


if __name__ == "__main__":
    main()