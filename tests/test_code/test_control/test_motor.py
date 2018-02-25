from src.code.control.motor import Motor
from src.testing.output_capture import TestHelpers

import ev3dev.ev3 as ev3
import pytest

class TestMotor:
        
    def test_simple_motor(self):
        def test_code():
            m = Motor('A')
            m . run(10, 10)

        test_output = TestHelpers() . get_motor_output(test_code)

        assert {
            'A': [
                {
                    'speed': '10',
                    'duration': '0.01'
                }
            ]
        } == test_output
                
    # def test_polarity(self):
    #     def test_code():
    #         m = Motor('A', -1)
    #         m . run(10, 10)

    #     test_output = TestHelpers() . get_motor_output(test_code)

    #     assert {
    #         'A': [
    #             {
    #                 'speed': '-10',
    #                 'duration': '0.01'
    #             }
    #         ]
    #     } == test_output

    def test_two_motors(self):
        def code():
            m = Motor('A')
            m2 = Motor('B')
            m . run(10, 10)
            m2 . run(100, 100)

        test_output = TestHelpers() . get_motor_output(code)

        assert {
            'A': [
                {
                    'speed': '10',
                    'duration': '0.01'
                }
            ],
            'B': [
                {
                    'speed': '100',
                    'duration': '0.1'
                }
            ]
        } == test_output
            