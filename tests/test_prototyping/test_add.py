'''
Template for testing file for sdp project
Team 6 - Lambda R

Important notes:

1. Test cases must always start with test_<testname>
2. Use assert for testing. Pytest will include nice details if a test fails
   Do not use anything else, python is smart enough to correctly compare objects
   So no fancy .equals or anything as with Jave
'''

# Import packages required for testing
from src.prototyping.adder import Adder

#Import pytest (required)
import pytest


# Can have inline tests.
def test_inline():
    a = Adder()
    assert a.dd(1, 2) == 3

# Can have test classes, the name must be Test<ClassName>
class TestAdder(object):
    # Simple test, expected to pass
    def test_one(self):
        a = Adder()
        assert a.add(1,2) == 3

    # If we want test code that raises errors
    # Use a context manager and the type of error you expect
    def test_will_throw(self):
        a = Adder()
        with pytest.raises(RuntimeError):
            a.subtract(1, 2)

    #If we expect a test to fail, use this annotation
    @pytest.mark.xfail()
    def test_will_fail(self):
        a = Adder()
        assert a.multiply(1, 2) == 2
