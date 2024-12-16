import pytest
import json
import os

from lab1.task1 import encryption, create_vigenere_ciphe, create_dict
from lab1.task2 import frequency_analysis_of_text, decryption
from lab1.working_functions import read_file, write_file, read_json, write_json


@pytest.fixture
def temp_file(tmp_path):
    file_path = tmp_path / "test.txt"
    yield file_path
    if os.path.exists(file_path):
        os.remove(file_path)

@pytest.fixture
def temp_json_file(tmp_path):
    file_path = tmp_path / "test.json"
    yield file_path
    if os.path.exists(file_path):
        os.remove(file_path)


@pytest.fixture
def temp_files(tmp_path):
    source_file = tmp_path / "source.txt"
    key_file = tmp_path / "key.txt"
    encrypted_file = tmp_path / "encrypted.txt"
    yield source_file, key_file, encrypted_file
    for file in [source_file, key_file, encrypted_file]:
        if os.path.exists(file):
            os.remove(file)


def test_read_file_exists(temp_file):
    test_text = "НЕ ВЫХОДИ ИЗ КОМНАТЫ"
    with open(temp_file, "w", encoding="utf-8") as f:
        f.write(test_text)
    assert read_file(temp_file) == test_text


def test_read_file_not_exists():
    assert read_file("nonexistent_file.txt") is None


def test_write_file(temp_file):
    test_text = "НЕ ВЫХОДИ ИЗ КОМНАТЫ"
    write_file(temp_file, test_text)
    with open(temp_file, "r", encoding="utf-8") as f:
        assert f.read() == test_text


def test_read_json_exists(temp_json_file):
    test_data = {"key1": "value1", "key2": "value2"}
    with open(temp_json_file, "w", encoding="utf-8") as f:
        json.dump(test_data, f)
    assert read_json(temp_json_file) == test_data


def test_read_json_not_exists():
    assert read_json("nonexistent_file.json") is None


def test_write_json(temp_json_file):
    test_data = {"key3": "value3", "key4": "value4"}
    write_json(temp_json_file, test_data)
    with open(temp_json_file, "r", encoding="utf-8") as f:
        assert json.load(f) == test_data
 

def test_create_dict():
    alphabet = "ABCDEFG"
    expected_dict = {"A": 0, "B": 1, "C": 2, "D": 3, "E": 4, "F": 5, "G": 6}
    assert create_dict(alphabet) == expected_dict


def test_create_vigenere_ciphe():
    alphabet = "ABC"
    expected_table = {
        0: ['A', 'B', 'C'],
        1: ['B', 'C', 'A'],
        2: ['C', 'A', 'B']
    }
    assert create_vigenere_ciphe(alphabet) == expected_table


@pytest.mark.parametrize("text, key, expected", 
                        [("НЕВЫХОДИИЗКОМНАТЫ", "БРОДСКИЙ", "ОХРЯЖШМСЙЧШТЭЧИЫЬ")])
def test_encryption(temp_files, text, key, expected):
    source_file, key_file, encrypted_file = temp_files
    write_file(source_file, text)
    write_file(key_file, key)
    encryption(source_file, key_file, encrypted_file)
    new_text = read_file(encrypted_file)
    assert new_text == expected


@pytest.mark.parametrize("expected, key, text", 
                        [("НЕ ВЫХОДИ ИЗ КОМНАТЫ", 
                          { "з":"Н", "4": "Е", "^": " ", "W":"В", "L": "Ы", "0": "Х", "х": "О", \
                            "X":"Д", "n": "И", "8": "З", "2": "К", "П": "М", "Р": "А", "!": "Т", "R": "Ы" }, 
                          "з4^WL0хXn^n8^2хПзР!R")])
def test_decryption(temp_files, expected, key, text):
    source_file, key_file, encrypted_file = temp_files
    write_file(encrypted_file, text)
    write_json(key_file, key)
    decryption(source_file, key_file, encrypted_file)
    new_text = read_file(source_file)
    assert new_text == expected


@pytest.mark.parametrize("text, expected_frequency", 
                         [("з4^WL0хXn^n8^2хПзР!R", 
                           {"з": 0.1, "4": 0.05, "^": 0.15, "W": 0.05, "L": 0.05, "0": 0.05, "х": 0.1, \
                            "X": 0.05, "n": 0.1, "8": 0.05, "2": 0.05, "П": 0.05, "Р": 0.05, "!": 0.05, "R": 0.05})])
def test_frequency(temp_json_file, expected_frequency, text):
    frequency_analysis_of_text(temp_json_file, text)
    new_dict = read_json(temp_json_file)
    assert new_dict == expected_frequency
 