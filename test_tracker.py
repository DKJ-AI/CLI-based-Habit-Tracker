import pytest
import json
import os
from datetime import datetime, timedelta
from tracker import HabitTracker


@pytest.fixture
def tracker(tmp_path, monkeypatch):
    monkeypatch.chdir(tmp_path)
    return HabitTracker()


# ─────────────────────────────────────────
# LOAD DATA TESTS
# ─────────────────────────────────────────

def test_load_valid_file(tmp_path, monkeypatch):
    monkeypatch.chdir(tmp_path)
    data = {"Gym": {"streak": 3, "last_done": "2026-04-11"}}
    with open('habit.json', 'w') as f:
        json.dump(data, f)
    t = HabitTracker()
    assert t.data == data


def test_load_data_empty_file(tmp_path, monkeypatch):
    monkeypatch.chdir(tmp_path)
    open('habit.json', 'w').close()
    t = HabitTracker()
    assert t.data == {}


def test_load_data_corrupted_file(tmp_path, monkeypatch):
    monkeypatch.chdir(tmp_path)
    with open('habit.json', 'w') as f:
        f.write("not valid json")
    t = HabitTracker()
    assert t.data == {}



# ─────────────────────────────────────────
# SAVE DATA TESTS
# ─────────────────────────────────────────

def test_save_data_overwrites_old(tracker):
    tracker.data = {"Old": {"streak": 1, "last_done": None}}
    tracker.save_data()
    tracker.data = {"New": {"streak": 2, "last_done": "2026-04-12"}}
    tracker.save_data()
    with open(tracker.filename, 'r') as f:
        result = json.load(f)
    assert "Old" not in result
    assert "New" in result

# ─────────────────────────────────────────
# MARK DONE TESTS
# ─────────────────────────────────────────

def test_mark_done_first_time(tracker):
    tracker.data = {"Gym": {"streak": 0, "last_done": None}}
    tracker.mark_done("Gym")
    assert tracker.data['Gym']['streak'] == 1
    assert tracker.data['Gym']['last_done'] == str(datetime.today().date())


def test_mark_done_consecutive_day(tracker):
    yesterday = str(datetime.today().date() - timedelta(days=1))
    tracker.data = {"Gym": {"streak": 3, "last_done": yesterday}}
    tracker.mark_done("Gym")
    assert tracker.data['Gym']['streak'] == 4


def test_mark_done_streak_broken(tracker):
    old_date = str(datetime.today().date() - timedelta(days=5))
    tracker.data = {"Gym": {"streak": 10, "last_done": old_date}}
    tracker.mark_done("Gym")
    assert tracker.data['Gym']['streak'] == 1


# ─────────────────────────────────────────
# DELETE HABIT TESTS
# ─────────────────────────────────────────

def test_delete_existing_habit(tracker):
    tracker.data = {
        "Gym": {"streak": 3, "last_done": "2026-04-12"},
        "Study": {"streak": 1, "last_done": "2026-04-11"}
    }
    tracker.delete_habit("Gym")
    assert "Gym" not in tracker.data
    assert "Study" in tracker.data


def test_delete_only_habit(tracker):
    tracker.data = {"Gym": {"streak": 5, "last_done": "2026-04-12"}}
    tracker.delete_habit("Gym")
    assert tracker.data == {}


def test_delete_nonexistent_habit(tracker, capsys):
    tracker.data = {"Gym": {"streak": 2, "last_done": "2026-04-12"}}
    tracker.delete_habit("Ghost")
    captured = capsys.readouterr()
    assert "not found" in captured.out.lower()
    assert "Gym" in tracker.data


# ─────────────────────────────────────────
# VIEW HABITS TESTS
# ─────────────────────────────────────────

def test_view_habits_empty(tracker, capsys):
    tracker.data = {}
    tracker.view_habits()
    captured = capsys.readouterr()
    assert "No habits found" in captured.out


def test_view_habits_shows_all(tracker, capsys):
    tracker.data = {
        "Gym": {"streak": 3, "last_done": "2026-04-12"},
        "Read": {"streak": 1, "last_done": "2026-04-11"}
    }
    tracker.view_habits()
    captured = capsys.readouterr()
    assert "Gym" in captured.out
    assert "Read" in captured.out