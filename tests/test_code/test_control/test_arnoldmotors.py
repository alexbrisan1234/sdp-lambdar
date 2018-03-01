from src.code.control.motor import ArnoldMotors
from src.testing.output_capture import TestHelpers

import pytest

class TestArnoldMotors:
    @pytest.mark.xfail()
    def test_move_forwards(self):
        def code():
            portDict = dict(
                frontLeft='A',
                frontRight='B',
                rearLeft='C',
                rearRight='D'
            )
            arnold = ArnoldMotors(portDict)
            arnold . move_forwards(1000, 100)

        test_output = TestHelpers() . get_motor_output(code)

        expected_inner_dict = dict(
            speed='100',
            duration='1.0'
        )
        
        expected_value = {
            'A': [expected_inner_dict],
            'B': [expected_inner_dict],
            'C': [expected_inner_dict],
            'D': [expected_inner_dict]
        }

        assert expected_value == test_output
    @pytest.mark.xfail()
    def test_move_backwards(self):
        def code():
            portDict = dict(
                frontLeft='A',
                frontRight='B',
                rearLeft='C',
                rearRight='D'
            )
            arnold = ArnoldMotors(portDict)
            arnold . move_backwards(1000, 100)

        test_output = TestHelpers() . get_motor_output(code)

        expected_inner_dict = dict(
            speed='-100',
            duration='1.0'
        )
        
        expected_value = {
            'A': [expected_inner_dict],
            'B': [expected_inner_dict],
            'C': [expected_inner_dict],
            'D': [expected_inner_dict]
        }

        assert expected_value == test_output

    @pytest.mark.xfail()
    def test_turn(self):
        def code():
            portDict = dict(
                frontLeft='A',
                frontRight='B',
                rearLeft='C',
                rearRight='D'
            )
            arnold = ArnoldMotors(portDict)
            arnold . turn(1000, 100, 50)

        test_output = TestHelpers() . get_motor_output(code)

        expected_inner_dict_left = dict(
            speed='100',
            duration='1.0'
        )

        expected_inner_dict_right = dict(
            speed='50',
            duration='1.0'
        )
        
        expected_value = {
            'A': [expected_inner_dict_left],
            'B': [expected_inner_dict_right],
            'C': [expected_inner_dict_left],
            'D': [expected_inner_dict_right]
        }

        assert expected_value == test_output
