# 🔥 Habit Tracker

> Build streaks. Break patterns. Show up every day.

A lightweight command-line habit tracker built in Python. Track your daily habits, maintain streaks, and never lose progress — all stored locally in a clean JSON file.

---

## ✨ Features

- ✅ Add habits with a name of your choice
- 🔥 Automatic streak tracking — consecutive days = growing streak
- 💀 Streak reset logic — miss a day and it resets to 1
- 🚫 Duplicate protection — can't add the same habit twice
- 🗑️ Delete habits cleanly
- 📋 Number-based selection — no typing habit names, pick by number
- 📊 Weekly report — see which habits are active or inactive this week
- 💾 Persistent JSON storage — data survives between sessions
- 🧪 pytest test suite included

---

## 🚀 Getting Started

### Prerequisites
- Python 3.6+
- No external dependencies (stdlib only)

### Installation

```bash
git clone https://github.com/DKJ-AI/habitflow.git
cd habitflow
python tracker.py
```

### Running Tests

```bash
pip install pytest
pytest test_tracker.py -v
```

---

## 🎮 Usage

```
1. Add Habit          → Add a new habit to track
2. View Habits        → See all habits with current streaks
3. Mark Done          → Pick a habit by number and mark it done today
4. Delete Habit       → Remove a habit permanently
5. Weekly Report      → See active/inactive status for the past 7 days
6. Exit
```

---

## 📁 Project Structure

```
habitflow/
├── tracker.py        # Core logic — HabitTracker class
├── test_tracker.py   # pytest test suite
├── habit.json        # Auto-generated data file
└── README.md
```

---

## 🗃️ Data Format

```json
{
    "Gym": {
        "streak": 3,
        "last_done": "2026-05-05"
    },
    "Coding": {
        "streak": 7,
        "last_done": "2026-05-05"
    }
}
```

---

## 🛠️ Built With

- Python 3
- `json` — data persistence
- `datetime` — streak logic
- `pytest` — testing
