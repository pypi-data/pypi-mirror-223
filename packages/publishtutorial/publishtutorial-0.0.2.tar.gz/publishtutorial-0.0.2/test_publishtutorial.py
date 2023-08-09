from myfunc import say_hello, average

def test_publishtutorial_no_params():
    assert say_hello() == "Hello, World!"

def test_publishtutorial_with_params():
    assert say_hello("Everyone") == "Hello, Everyone!"

def test_average():
    assert average(1,2) == 1.5