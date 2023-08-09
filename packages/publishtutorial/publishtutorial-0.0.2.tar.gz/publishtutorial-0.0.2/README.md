# Publish package tutorial

## Installation
```bash
pip3 install publishtutorial
```

## Usage
```python
from myfunc import say_hello

# Generate "Hello, World!"
say_hello()

# Generate "Hello, Everybody!"
say_hello("Everybody")
```

## Developing
To install publishtutorial,
 along with the tools you need to develop and run tests,
 run the following in your virtualenv:
```bash
$ pip3 install -e .[dev]
```