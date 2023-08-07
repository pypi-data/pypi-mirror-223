import pytest
import datetime as dt
from surquest.utils.randomizer import Randomizer

class TestRandomizer:

    def test_get_current_timestamp(self):

        randomizer = Randomizer()
        now = round(dt.datetime.utcnow().timestamp())
        timestamp = randomizer.get_current_timestamp()
        
        assert isinstance(timestamp, int) == True
        assert timestamp == now

    def test_generate_random_charset_series(self):

        randomizer = Randomizer()
        series = randomizer.generate_random_charset_series(10)

        assert isinstance(series, dict) == True
        assert len(series.keys()) == 10
        for item in series.values():
            assert isinstance(item, list) == True
            assert len(item) == len(randomizer.CHARSET)

    def test_generate_timestamped_random_string(self):

        randomizer = Randomizer()
        string = randomizer.generate_timestamped_random_string(8)
        assert isinstance(string, str) == True, F"Expected string, got: {type(string)}"
        assert len(string) == 8, F"Expected string length: 8, got: {len(string)}"

    def test_generate_timestamped_random_string_value_error(self):

        randomizer = Randomizer()

        with pytest.raises(ValueError):
            randomizer.generate_timestamped_random_string(6)

        with pytest.raises(ValueError):
            randomizer.generate_timestamped_random_string(6, enforced_minimal_length=6)

    def test_generate_timestamped_random_string_uniqueness_2(self):

        randomizer = Randomizer()
        string1 = randomizer.generate_timestamped_random_string(8)
        string2 = randomizer.generate_timestamped_random_string(8)

        assert string1 != string2, F"Expected two different strings, got two identical strings: {string1} and {string2}"

    def test_generate_timestamped_random_string_uniqueness_1000(self):

        randomizer = Randomizer()

        n = 1000
        strings = set()
        for i in range(n):
            string = randomizer.generate_timestamped_random_string(8)
            strings.add(string)

        assert len(strings) == n, F"Expected {n} unique strings, got {len(strings)} unique strings."

    def test_generate_timestamped_random_string_uniqueness_100000(self):

        randomizer = Randomizer()

        n = 100000
        strings = set()
        for i in range(n):
            string = randomizer.generate_timestamped_random_string(10)
            strings.add(string)

        assert len(strings) == n, F"Expected {n} unique strings, got {len(strings)} unique strings."

    def test_generate_timestamped_random_string_uniqueness(self):

        randomizer = Randomizer()

        for i in [7, 8, 9]:
            
            random_set = set()
            unique_size = randomizer.charset_length**(i-6)
            for j in range(unique_size):
                random_set.add(
                    randomizer.generate_timestamped_random_string(i)
                    )
            assert len(random_set) == unique_size, F"Expected {unique_size} unique strings, got {len(random_set)} unique strings."

    def test_convert_charset_to_integer(self):

        randomizer = Randomizer()
        
        number = 1234567890

        charset = randomizer.convert_integer_to_charset(number=number)
        
        number_out = randomizer.convert_charset_to_integer(charset)

        assert number_out == number, F"Original number: {number}, converted number: {number_out}"

