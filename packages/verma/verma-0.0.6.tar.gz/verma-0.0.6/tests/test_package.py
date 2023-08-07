

def test_can_import():
    from verma import say_hello

    assert say_hello() == 'hello'