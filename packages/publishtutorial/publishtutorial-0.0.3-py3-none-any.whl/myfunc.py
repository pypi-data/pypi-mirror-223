def say_hello(name=None):
    if name is None:
        return "Hello, World!"
    else:
        return f"Hello, {name}!"
    
def average(a:float=1, b:float=2) -> float:
    return (a+b)/2