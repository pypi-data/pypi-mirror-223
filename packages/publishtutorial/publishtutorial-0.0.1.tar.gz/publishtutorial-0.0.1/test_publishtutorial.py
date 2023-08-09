from myfunc import say_hello

def test_publishtutorial_no_params():
    assert say_hello() == "Hello, World!"

def test_publishtutorial_with_params():
    assert say_hello("Everyone") == "Hello, Everyone!"