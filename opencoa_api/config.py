from dataclasses import dataclass
from pyrad.dictionary import Dictionary

RETURN_CODES = {
    1: "AccessRequest",
    2: "AccessAccept",
    3: "AccessReject",
    4: "AccountRequest",
    5: "AccountingResponse",
    11: "AccessChallenge",
    12: "StatusServer",
    13: "StatusClient",
    40: "DisconnectRequest",
    41: "DisconnectACK",
    42: "DisconnectNAK",
    43: "COARequest",
    44: "COAACK",
    45: "COANAK",
}


@dataclass
class Config:
    RADIUS_DICTIONARY_PATH: str
    RADIUS_DICTIONARY: Dictionary = None
    API_PORT: int = 8080

    def load_dictionary(self) -> None:
        """Loads the dictionary of Radius attributes based on the RADIUS_DICTIONARY_PATH/dictionary file"""
        self.RADIUS_DICTIONARY = Dictionary(f"{self.RADIUS_DICTIONARY_PATH}/dictionary")

    def validate_attribute(self, attribute: str) -> bool:
        """Validates if the given attribute exists in the default RADIUS_DICTIONARY

        Arguments:
            attribute:  Radius Attribute Key

        Returns True if attribute is valid, False if invalid"""
        if self.RADIUS_DICTIONARY.attributes.get(attribute) is None:
            return False
        return True

    def validate_attributes(self, attributes: dict) -> list:
        """Validates if the given attributes exists in the default RADIUS_DICTIONARY

        Arguments:
            attributes: dict of attributes { 'Attribute-Key': 'AttributeValue'}

        Returns the list of unsupported attributes"""
        unsupported_attributes = []
        for attribute in attributes:
            if self.RADIUS_DICTIONARY.attributes.get(attribute) is None:
                unsupported_attributes.append(attribute)
        return unsupported_attributes

    def normalize_attributes(self, attributes: dict) -> dict:
        """Normalizes attributes stored in the dictionary with underscores (_)

        Arguments:
            attributes: dict of attributes { 'Attribute-Key': 'AttributeValue'}

        Returns dict of attributes normalized"""
        return {k.replace("-", "_"): attributes[k] for k in attributes}

    def get_return_code_description(self, code: int) -> dict:
        """Finds a description based on common return codes

        Arguments:
            code:   Radius Type Code

        Returns value if code exist"""
        return RETURN_CODES.get(code)
