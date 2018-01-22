class Adder(object):
    def add(self, x, y):
        return x + y

    def subtract(self, x, y):
        raise RuntimeError('This is expected to happen')

    def multiply(self, x, y):
        return x / y
