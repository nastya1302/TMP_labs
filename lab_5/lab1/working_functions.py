import json
import logging

from lab1.const import LOG

logging.basicConfig(level=logging.INFO, 
                    format="%(asctime)s %(levelname)s %(message)s", 
                    filename=LOG, 
                    filemode="w")  

def read_file(path: str) -> str:
    """
    A function for reading a file. accepts a path as input, returns a string.
    """
    logging.info(f"Reading file: {path}")
    try:
        with open(path, "r", encoding="utf-8") as f:
            text = f.read()
        logging.info(f"File '{path}' read successfully.")
        return text
    except FileNotFoundError as e:
        logging.error(f"Error reading file '{path}': {e}")
        return None


def write_file(path: str, text: str) -> None:
    """
    A function for writing to a file using a specified path.
    """
    logging.info(f"Writing to file: {path}")
    try:
        with open(path, "w", encoding="utf-8") as f:
            f.write(text)
        logging.info(f"File '{path}' written successfully.")
    except Exception as e:
        logging.exception(f"An error occurred while writing to '{path}': {e}")


def read_json(path: str) -> dict:
    """
    A function for reading a .json file. accepts a path as input, returns a dictionary.
    """
    logging.info(f"Reading .json file: {path}")
    try:
        with open(path, "r", encoding="UTF-8") as f:
            text = json.load(f)
        logging.info(f"A .json file '{path}' read successfully.")
        return text
    except FileNotFoundError as e:
        logging.error(f"Error reading .json file '{path}': {e}")
        return None


def write_json(path: str, dictionary: dict) -> None:
    """
    A function for writing to a file using a specified path.
    """
    logging.info(f"Writing to .json file: {path}")
    try:
        with open(path, 'w', encoding="UTF-8") as f:
            json.dump(dictionary, f, ensure_ascii=False,)
        logging.info(f"A .json file '{path}' written successfully.")
    except Exception as e:
        logging.exception(f"An error occurred while writing to '{path}': {e}")
 