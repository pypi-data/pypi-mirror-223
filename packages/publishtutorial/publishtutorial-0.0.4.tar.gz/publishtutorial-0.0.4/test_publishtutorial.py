from myfunc import say_hello, average
from second_script import second_function

def test_publishtutorial_no_params():
    assert say_hello() == "Hello, World!"

def test_publishtutorial_with_params():
    assert say_hello("Everyone") == "Hello, Everyone!"

def test_average_no_params():
    assert average() == 1.5

def test_average_with_params():
    assert average(3,2) == 2.5

def test_second_no_params():
    assert second_function() == 2.5

def test_second_with_params():
    assert second_function(3) == 5.5