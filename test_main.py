import pytest
import os
import json
from datetime import datetime, timedelta
from unittest.mock import patch, mock_open
from main import load_data, save_data, add_habit_to_json, view_habits, mark_done


# LOAD DATA TESTS

def test_load_data_file_not_exists():
  if os.path.exists('habit.json'):
    os.remove('habit.json')
  result = load_data()
  assert result == {}


def test_load_valid_files(tmp_path, monkeypatch):
  monkeypatch.chdir(tmp_path)
  data = {"Gym": {"streak": 3, "last_done": "2026-04-11"}}
  with open('habit.json', 'w') as f:
    json.dump(data, f)
  result = load_data()
  assert result == data


def test_load_data_empty_file(tmp_path, monkeypatch):
  monkeypatch.chdir(tmp_path)
  open('habit.json', 'w').close()
  result = load_data()
  assert result == {}


def test_load_data_corrupted_file(tmp_path, monkeypatch):
  monkeypatch.chdir(tmp_path)
  with open('habit.json', 'w') as f:
    f.write("this is not json {{{{")
  result = load_data()
  assert result == {}


def test_load_data_wrong_type(tmp_path, monkeypatch):
  monkeypatch.chdir(tmp_path)
  with open('habit.json', 'w') as f:
    json.dump([1, 2, 3], f)
  result = load_data()
  assert result == {}



# SAVE DATA TESTS

def test_save_data_writes_correctly(tmp_path, monkeypatch):
  monkeypatch.chdir(tmp_path)
  data = {"Gym": {"streak": 5, "last_done": "2026-04-12"}}
  save_data(data)
  with open('habit.json', 'r') as f:
    result = json.load(f)
  assert result == data


def test_save_data_overwrites_old(tmp_path, monkeypatch):
  monkeypatch.chdir(tmp_path)
  save_data({"Old": {"streak": 1, "last_done": None}})
  new_data = {"New": {"streak": 2, "last_done": "2026-04-12"}}
  save_data(new_data)
  with open('habit.json', 'r') as f:
    result = json.load(f)
  assert result == new_data
  assert "Old" not in result



# ADD HABIT TESTS

def test_add_habit_new(tmp_path, monkeypatch):
  monkeypatch.chdir(tmp_path)
  with patch('builtins.input', return_value='Gym'):
    add_habit_to_json()
  result = load_data()
  assert 'Gym' in result
  assert result['Gym']['streak'] == 0
  assert result['Gym']['last_done'] is None


def test_add_habit_duplicate(tmp_path, monkeypatch, capsys):
  monkeypatch.chdir(tmp_path)
  save_data({"Gym": {"streak": 2, "last_done": "2026-04-12"}})
  with patch('builtins.input', return_value='Gym'):
    add_habit_to_json()
  captured = capsys.readouterr()
  assert "already exists" in captured.out
  result = load_data()
  assert result['Gym']['streak'] == 2


def test_add_multiple_habits(tmp_path, monkeypatch):
  monkeypatch.chdir(tmp_path)
  for name in ['Gym', 'Study', 'Read']:
    with patch('builtins.input', return_value=name):
      add_habit_to_json()
  result = load_data()
  assert 'Gym' in result
  assert 'Study' in result
  assert 'Read' in result


# MARK DONE TESTS

def test_mark_done_first_time(tmp_path, monkeypatch):
  monkeypatch.chdir(tmp_path)
  save_data({"Gym": {"streak": 0, "last_done": None}})
  with patch('builtins.input', return_value='Gym'):
    mark_done()
  result = load_data()
  assert result['Gym']['streak'] == 1
  assert result['Gym']['last_done'] == str(datetime.today().date())


def test_mark_done_consecutive_day(tmp_path, monkeypatch):
  monkeypatch.chdir(tmp_path)
  yesterday = str(datetime.today().date() - timedelta(days=1))
  save_data({"Gym": {"streak": 3, "last_done": yesterday}})
  with patch('builtins.input', return_value='Gym'):
    mark_done()
  result = load_data()
  assert result['Gym']['streak'] == 4


def test_mark_done_streak_broken(tmp_path, monkeypatch):
  monkeypatch.chdir(tmp_path)
  old_date = str(datetime.today().date() - timedelta(days=5))
  save_data({"Gym": {"streak": 10, "last_done": old_date}})
  with patch('builtins.input', return_value='Gym'):
    mark_done()
  result = load_data()
  assert result['Gym']['streak'] == 1


def test_mark_done_already_today(tmp_path, monkeypatch, capsys):
  monkeypatch.chdir(tmp_path)
  today = str(datetime.today().date())
  save_data({"Gym": {"streak": 3, "last_done": today}})
  with patch('builtins.input', return_value='Gym'):
    mark_done()
  captured = capsys.readouterr()
  assert "Already marked done today" in captured.out


def test_mark_done_habit_not_found(tmp_path, monkeypatch, capsys):
  monkeypatch.chdir(tmp_path)
  save_data({"Gym": {"streak": 1, "last_done": None}})
  with patch('builtins.input', return_value='NonExistentHabit'):
    mark_done()
  captured = capsys.readouterr()
  assert "not found" in captured.out.lower()