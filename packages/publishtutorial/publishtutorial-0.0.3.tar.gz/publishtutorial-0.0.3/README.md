# Publish package tutorial

## Installation
Create a virtualenv and then install the library
```bash
pip3 install publishtutorial
```

## Usage
```python
from myfunc import say_hello, average

# Generate "Hello, World!"
say_hello()

# Generate "Hello, Everybody!"
say_hello("Everybody")

# Compute average between two numbers (default values are 1 and 2)
average()

# Compute average between two numbers (2.5)
average(2,3)
```

## Developing
To install publishtutorial,
 along with the tools you need to develop and run tests,
 run the following in your virtualenv:
```bash
$ pip3 install -e .[dev]
```


Credits to: [Coding Tech](https://www.youtube.com/watch?v=GIF3LaRqgXo&t=3s)