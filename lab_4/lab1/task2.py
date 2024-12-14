from working_functions import *
from const import PATH, LOG

logging.basicConfig(level=logging.INFO, 
                    format="%(asctime)s %(levelname)s %(message)s", 
                    filename=LOG, 
                    filemode="w") 

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
    logging.info("The frequency analysis of the specified ciphertext has been completed.")    


def decryption(path_sourse_text: str, path_key: str, path_encrypted_text: str, path_text_analysis: str) -> None:
    """
    A function for creating decrypted text.
    """
    logging.info(f"Starting decryption. Source text: {path_encrypted_text}, key: {path_key}, output: {path_sourse_text}") 
    try:   
        text: str = read_file(path_encrypted_text)
        key: dict = read_json(path_key)
        frequency_analysis_of_text(path_text_analysis, text)
        new_text: str = ""
        for letter in text:
            if letter in key:
                new_text += key[letter]
        write_file(path_sourse_text, new_text)
        logging.info(f"Decryption completed successfully. Decrypted text saved to: {path_sourse_text}")
    except Exception as e:
        logging.exception(f"An error occurred during decryption: {e}")        


def main() -> None:
    paths: dict = read_json(PATH)
    decryption(
        paths["task2_sourse_text"], paths["task2_key"], paths["task2_encrypted_text"], paths["task2_text_analysis"]
    )


if __name__ == "__main__":
    main()
 