![GitHub](https://img.shields.io/github/license/surquest/python-random-generator?style=flat-square)
![GitHub Workflow Status (with branch)](https://img.shields.io/github/actions/workflow/status/surquest/python-random-generator/test.yml?branch=main&style=flat-square)
![Coverage](https://img.shields.io/endpoint?url=https://gist.githubusercontent.com/surquest/6e25c317000917840152a5e702e71963/raw/python-random-generator.json&style=flat-square)
![PyPI - Downloads](https://img.shields.io/pypi/dm/surquest-utils-random-string-generator?style=flat-square)
![PyPI](https://img.shields.io/pypi/v/surquest-utils-random-string-generator)


# Introduction

This package provides a simple way how to generate timestamped random strings with minimal length of 8 characters. The first 6 characters are the timestamp in seconds and the remaining set of characters (required length - 6) are randomly generated. 

The random string is generated using the following set of characters: `abcdefghijkmnopqrstuvwxyzABCDEFGHJKLMNPQRSTUVWXYZ23456789` as you can see the characters `l` and `I` are not included to avoid confusion with `1` and `0`.

The key advantage of this package is the ability to generate completely unique and not easily predictible strings with the performace:

-  57 strings per 1 seconds for a length of 7 characters
-  3,249 strings per 1 seconds for a length of 8 characters
-  185,193 strings per 1 seconds for a length of 9 characters

# Usage

```python
# import the randomizer
from surquest.utils.randomizer import Randomizer

# Generate a timestamped random string with a length of 8 characters
random_string = Randomizer.generate_timestamped_random_string(
    string_length=8
) # returns something like `gechEuKq`
```

# Installation

The package is available on PyPI and can be installed using pip:

```
pip install surquest-utils-random-string-generator
```

# Additional information

You are also able to submit your own set of characters to be used for the random string generation.

```python
import string
from surquest.utils.randomizer import Randomizer

# Generate a timestamped random string with a length of 8 characters

randomizer = Randomizer(
    string_length=8,
    characters=string.ascii_letters + string.digits
)

random_string = randomizer.generate_timestamped_random_string(10)
```

The Randomizer class can be also used for conversion of integers to strings based on given set of characters.

```python
from surquest.utils.randomizer import Randomizer

randomizer = Randomizer()

# input number
number = 1234567890

# convert number to string
random_string = randomizer.convert_integer_to_charset(number)

# convert string back to number
number = randomizer.convert_charset_to_integer(random_string)
```

# Local development

You are more than welcome to contribute to this project. To make your start easier we have prepared a docker image with all the necessary tools to run it as interpreter for Pycharm or to run tests.

## Build docker image
```powershell
# powershell syntax (windows)
docker build `
 --tag surquest/utils/randomizer `
 --file package.base.dockerfile `
 --target test .
```

## Run tests
```powershell
# powershell syntax (windows)
docker run --rm -it `
 -v "${pwd}:/opt/project" `
 -w "/opt/project/test" `
 surquest/utils/randomizer pytest
```