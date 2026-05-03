# 🔥 HabitFlow — CLI Habit Tracker

> Build streaks. Break patterns. Show up every day.

A lightweight command-line habit tracker built in Python. Track your daily habits, maintain streaks, and never lose progress — all stored locally in a clean JSON file.

---

## 📸 Demo

<!-- REPLACE THESE with your actual screenshots -->
<img width="692" height="290" alt="Screenshot 2026-04-13 020741" src="https://github.com/user-attachments/assets/0c9e70c5-ecb1-489f-a79a-fd27c14f2d12" />

<img width="648" height="177" alt="Screenshot 2026-04-13 020805" src="https://github.com/user-attachments/assets/a345051e-003d-4a15-8aca-ae14e1b37429" />

<img width="565" height="123" alt="Screenshot 2026-04-13 020913" src="https://github.com/user-attachments/assets/53b51f8d-a693-4e42-be91-d2e21b0be3f6" />



---

## ✨ Features

- ✅ Add habits with a single command
- 🔥 Automatic streak tracking — consecutive days = growing streak
- 💀 Streak reset logic — miss a day and it resets to 1
- 🚫 Duplicate protection — can't add the same habit twice
- 🗑️ Delete habits cleanly
- 💾 Persistent JSON storage — data survives between sessions
- 🧪 Full pytest test suite included

---

## 🚀 Getting Started

### Prerequisites
- Python 3.6+
- No external dependencies (stdlib only)

### Installation

```bash
git clone https://github.com/YOUR_USERNAME/habitflow.git
cd habitflow
python main.py
```

### Running Tests

```bash
pip install pytest
pytest test_main.py -v
```

---

## 🎮 Usage

```
1. Add Habit       → Add a new habit to track
2. View Habits     → See all habits with current streaks
3. Mark Done       → Mark today's habit complete
4. Delete Habit    → Remove a habit permanently
5. Exit
```

---

## 📁 Project Structure

```
habitflow/
├── main.py          # Core logic — all functions
├── test_main.py     # pytest test suite (20 tests)
├── habit.json       # Auto-generated data file
└── README.md
```

---

## 🗃️ Data Format

```json
{
    "Gym": {
        "streak": 3,
        "last_done": "2026-04-13"
    },
    "Coding": {
        "streak": 7,
        "last_done": "2026-04-13"
    }
}
```

---

## 🧪 Test Coverage

| Module | Tests |
|--------|-------|
| `load_data` | File not found, valid file, empty file, corrupted JSON, wrong type |
| `save_data` | Writes correctly, overwrites old data |
| `add_habit` | New habit, duplicate blocked, multiple habits |
| `mark_done` | First time, consecutive streak, broken streak, already done today, not found |
| `delete_habit` | Existing habit, only habit, nonexistent, preserves other streaks |

---

## 🛠️ Built With

- Python 3
- `json` — data persistence
- `datetime` — streak logic
- `pytest` — testing

---

## 👤 Author

**Dipak Jena**
- GitHub: DKJ-AI(https://github.com/DKJ-AI)

