import json
import csv
import re


def read_json(path: str) -> dict[str, str]:
    """
    A function for reading a .json file. Accepts a path as input, returns a dictionary.
    
    Args:
        path (str): path to a .json file.

    Returns:
        dict[str, str]: data dictionary.
    """
    try:
        with open(path, "r", encoding="UTF-8") as f:
            text = json.load(f)
        return text
    except FileNotFoundError as e:
        print(e)


def write_json(path: str, dictionary: dict[str, str]) -> None:
    """
    A function for writing to a file using a specified path.

    Args:
        path (str): path to a .json file;
        dictionary [str, str]: dictionary of data to be entered in the file.
    """
    try:
        with open(path, 'w') as f:
            json.dump(dictionary, f)
    except Exception as e:
        print(e)


def read_csv(path: str) -> list[list[str]]:
    """
    A function reads data from a .csv file.

    Args:
        path (str): path to a .csv file.

    Returns:
        list[list[str]]: .csv file lines.
    """
    try:
        list_data: list[list[str]] = []
        with open(path, "r", encoding="utf-16") as f:
            reader = csv.reader(f, delimiter=";")
            next(reader, None)
            for row in reader:
                list_data.append(row)
            return list_data
    except Exception as e:
        print(e)


def validation_check(patterns: dict[str, str], list_data: list[str]) -> bool:
    """
    The function checks the text using patterns.

    Args:
        patterns (dict[str, str]): patterns for data processing;
        list_data (list[str]): data from .csv files.

    Returns:
        bool: valid or invalid
    """
    for key, value in zip(patterns.keys(), list_data):
        if not re.match(patterns[key], value):
            return False
    return True


def get_invalid_data(patterns: dict[str, str], list_data: list[str]) -> list[int]:
    """
    A function creates a list with indexes of invalid data.

    Args:
        patterns (dict[str, str]): patterns for data processing;
        list_data (list[str]): data from .csv files.

    Returns:
        list[int]: indexes of invalid rows.
    """
    list_invalid: list[int] = []
    for index, row in enumerate(list_data[1:]):
        if not validation_check(patterns, row):
            list_invalid.append(index)
    return list_invalid
 