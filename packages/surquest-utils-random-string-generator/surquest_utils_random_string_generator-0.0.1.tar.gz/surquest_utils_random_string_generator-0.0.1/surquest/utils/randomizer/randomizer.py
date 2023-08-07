"""
This module provides a Randomizer class that generates random strings with a timestamp part in the pattern.
The class uses a charset of 50 characters (excluding l, I, 1, O, 0) to generate random strings.
The generated strings have a minimal length of 8 characters.
The class also provides methods to convert an integer to a charset string and vice versa.
"""
from typing import Optional, AnyStr
import datetime as dt
import random


import datetime as dt
import random
from typing import AnyStr, Optional

class Randomizer:
    """
    A class for generating random strings with a timestamp part.

    Attributes:
    - CHARSET (str): The default character set used for generating random strings.
    - charset (str): The character set used for generating random strings.
    - charset_length (int): The length of the character set.
    - counter (int): A counter used for generating random strings.
    - _timestamp (int): The current timestamp.
    - _regenerations (int): The number of times the character set has been regenerated.
    - _series (dict): A dictionary containing random character sets.
    """

    CHARSET = "abcdefghijkmnopqrstuvwxyzABCDEFGHJKLMNPQRSTUVWXYZ23456789"

    def __init__(self, charset: Optional[AnyStr] = None):
        """
        Initializes a new instance of the Randomizer class.

        Parameters:
        - charset (str): The character set used for generating random strings. If None, the default CHARSET is used.
        """
        self.charset = (
            charset if charset else "".join(self.randomize_charset(self.CHARSET))
        )
        self.charset_length = len(self.charset)
        self.counter = 0

        self._timestamp = self.get_current_timestamp()
        self._regenerations = 0
        self._series = self.generate_random_charset_series(length=0)

    @staticmethod
    def get_current_timestamp() -> int:
        """
        Returns the current timestamp.

        Returns:
        - int: The current timestamp.
        """
        return round(dt.datetime.utcnow().timestamp())

    def generate_random_charset_series(self, length: int) -> dict:
        """
        Generates a dictionary containing random character sets.

        Parameters:
        - length (int): The length of the dictionary.

        Returns:
        - dict: A dictionary containing random character sets.
        """
        series = {}
        for i in range(length):
            series[i] = self.randomize_charset(self.CHARSET)

        return series

    def generate_timestamped_random_string(
        self,
        string_length: int,
        pattern: str = "{timestamp}{random}",
        enforced_minimal_length=7,
    ) -> str:
        """
        Generates a random string with a timestamp part.

        Parameters:
        - string_length (int): The length of the random string.
        - pattern (str): The pattern of the random string. Defaults to "{timestamp}{random}".
        - enforced_minimal_length (int): The minimal length of the random string. Defaults to 8.

        Returns:
        - str: A random string with a timestamp part.
        """
        required_minimal_length = 7
        has_timestamp = True if "{timestamp}" in pattern else False

        if has_timestamp is True and enforced_minimal_length < required_minimal_length:
            raise ValueError(
                f"Random string with timestamp part in pattern needs to have minimal length: {required_minimal_length}"
            )

        if string_length < enforced_minimal_length:
            raise ValueError(
                f"Random string with needs to have minimal length: {enforced_minimal_length}"
            )

        timestamp_part = ""
        if has_timestamp is True:
            timestamp = self.get_current_timestamp()
            timestamp_part = self.convert_integer_to_charset(number=timestamp)

        timestamp_part_length = len(timestamp_part)
        random_part_length = string_length - timestamp_part_length

        if (
            random_part_length != len(self._series.keys())
            or timestamp != self._timestamp
        ):
            self._series = self.generate_random_charset_series(
                length=random_part_length
            )
            self._regenerations = 0
            self._timestamp = timestamp

        random_part = self.generate_random_part(
            number=self._regenerations,
            elements_count=random_part_length,
            charset_length=self.charset_length,
        )

        self._regenerations += 1

        out = pattern.format(random=random_part, timestamp=timestamp_part)

        return out

    def generate_random_part(self, number, elements_count, charset_length) -> str:
        """
        Generates a random part of a random string.

        Parameters:
        - number (int): A counter used for generating the random part.
        - elements_count (int): The length of the random part.
        - charset_length (int): The length of the character set.

        Returns:
        - str: A random part of a random string.
        """
        parts = list()
        while number > 0:
            remainder = number % charset_length
            number //= charset_length
            parts.append(remainder)

        if len(parts) != elements_count:
            parts += [0] * (elements_count - len(parts))

        out = []
        for idx, val in enumerate(parts):
            out.append(self._series[idx][val])

        return "".join(out)

    def convert_integer_to_charset(
        self, number: int, charset: Optional[AnyStr] = None
    ) -> str:
        """
        Converts an integer to a string using a character set.

        Parameters:
        - number (int): The integer to convert.
        - charset (str): The character set to use. If None, the instance's charset is used.

        Returns:
        - str: The converted string.
        """
        remainders = []
        charset = charset if charset else self.charset
        base = len(charset)

        while number > 0:
            remainder = number % base
            number //= base
            remainders.append(charset[remainder])

        out = "".join(remainders[::-1]) if len(remainders) > 0 else charset[0]

        return out

    def convert_charset_to_integer(
        self, string: str, charset: Optional[AnyStr] = None
    ) -> int:
        """
        Converts a string to an integer using a character set.

        Parameters:
        - string (str): The string to convert.
        - charset (str): The character set to use. If None, the instance's charset is used.

        Returns:
        - int: The converted integer.
        """
        charset = charset if charset else self.charset
        base = len(charset)

        # Create a dictionary to map each character to its index in the charset
        charset_index_map = {charset[i]: i for i in range(base)}

        number = 0
        for char in string:
            # Convert each character to its corresponding index in the charset and update the number
            number = number * base + charset_index_map[char]

        return number

    @staticmethod
    def randomize_charset(charset: str) -> str:
        """
        Randomizes a character set.

        Parameters:
        - charset (str): The character set to randomize.

        Returns:
        - str: The randomized character set.
        """
        return random.sample(charset, len(charset))