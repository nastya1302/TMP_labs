from working_functions import *
from const import PATH


def frequency_analysis_of_text(path: str, text: str) -> None:
    """
    A function for performing frequency analysis of a given ciphertext.
    """
    frequency = {}
    l = len(text)
    text_litters = []
    for i in text:
        if text_litters.count(i) == 0:
            text_litters.append(i)
    for i in text_litters:
        frequency[i] = text.count(i) / l
    write_json(path, frequency)


def decryption(path_sourse_text: str, path_key: str, path_encrypted_text: str, path_text_analysis: str) -> None:
    """
    A function for creating decrypted text.
    """
    text: str = read_file(path_encrypted_text)
    key: dict = read_json(path_key)
    frequency_analysis_of_text(path_text_analysis, text)
    new_text: str = ""
    for letter in text:
        if letter in key:
            new_text += key[letter]
    write_file(path_sourse_text, new_text)


def main() -> None:
    paths: dict = read_json(PATH)
    decryption(
        paths["task2_sourse_text"], paths["task2_key"], paths["task2_encrypted_text"], paths["task2_text_analysis"]
    )


if __name__ == "__main__":
    main()
 