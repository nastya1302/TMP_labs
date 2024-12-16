import logging

from lab1.working_functions import read_file, write_file, read_json, write_json
from lab1.const import *

logging.basicConfig(level=logging.INFO, 
                    format="%(asctime)s %(levelname)s %(message)s", 
                    filename=LOG, 
                    filemode="w") 

def create_dict(sourse_alphabet: str) -> dict:
    """
    A function for creating a dictionary from the alphabet. Accepts the alphabet as input, returns the dictionary.
    """
    dict_alphabet: dict = {}
    i: int = 0
    for letter in sourse_alphabet:
        dict_alphabet[letter] = i
        i += 1
    logging.info("Alphabet dictionary created successfully.")
    return dict_alphabet


def create_vigenere_ciphe(sourse_alphabet: str) -> dict:
    """
    A function for creating vigenere ciphe. Accepts the alphabet as input, returns the dictionary.
    """
    list_letter: list = list(sourse_alphabet)
    list_line: dict = {}
    count: int = len(list_letter)
    for i in range(count):
        list_line[i] = list_letter[i : i + count : 1] + list_letter[0:i]
    logging.info("Vigenere cipher table created successfully.")
    return list_line


def encryption(path_sourse_text: str, path_key: str, path_encrypted_text: str) -> None:
    """
    A function for creating encrypted text.
    """
    logging.info(f"Starting encryption. Source text: {path_sourse_text}, key: {path_key}, output: {path_encrypted_text}")
    try:
        text: str = read_file(path_sourse_text)
        key: str = read_file(path_key)
        if text is None or key is None:
            logging.error("Error reading source text or key file.")
            return
        text: str = "".join(text.split())
        key: str = (key * (len(text) // len(key) + 1))[: len(text)]
        dict_alphabet: dict = create_dict(ALPHABET)
        table: dict = create_vigenere_ciphe(ALPHABET)
        new_text: str = ""
        for k, t in zip(key, text):
            new_text += table[dict_alphabet[k]][dict_alphabet[t]]
        write_file(path_encrypted_text, new_text)
        logging.info(f"Encryption completed successfully. Encrypted text saved to: {path_encrypted_text}")
    except Exception as e:
        logging.exception(f"An error occurred during encryption: {e}")


def main() -> None:
    paths: dict = read_json(PATH)
    encryption(
        paths["task1_sourse_text"], paths["task1_key"], paths["task1_encrypted_text"]
    )


if __name__ == "__main__":
    main()
 