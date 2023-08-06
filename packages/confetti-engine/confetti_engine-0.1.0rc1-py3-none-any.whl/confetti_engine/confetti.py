import json
import logging as log

from attr import define, field

log.basicConfig(
    format="%(asctime)s - %(levelname)s - %(message)s",
    level=log.INFO
)


@define
class Datastore:
    """
    Confetti's data management module.
    """
    data = {}  # type: ignore # noqa: F401
    file: str = field(default="data.json")

    def prep(self, key: str, value: str, encrypt: bool = False):
        """
        Prepare the data to be stored in a JSON file set in Datastore() class
        :param key: Unique identifier for value or data
        :param value: To be set with the key and prepped to be stored
        :param encrypt: Encrypt value?
        Defaults to false.
        """
        if encrypt:
            log.warning("Encryption call was sent with prep function.")
            self.data[key] = "ENCRYPT-"+value
            log.info(f"Datastore prepped with key, ({key}) with the corresponding\033[31m encrypted\033[39m value of, "
                     f"({value})")
        else:
            self.data[key] = value
            log.info(f"Datastore prepped with key, ({key}) with the corresponding value of, ({value})")

    def save(self):
        """
        Saves identified data to json file set in prep() function
        """
        with open(self.file, 'w') as file:
            json.dump(self.data, file, indent=4)
            log.info("Datastore saved.")
            if self.file == "data.json":
                log.warning("Datastore was saved to default file. Please change it to your .json file.")

    def load(self):
        """
        Loads JSON file to have values ot be picked by unique identifier set in prep() function
        :return: JSON Data
        """
        with open(self.file, 'r') as file:
            log.info("Datastore opened.")
            data = json.load(file)
            log.info("Datastore loaded.")
        return data
