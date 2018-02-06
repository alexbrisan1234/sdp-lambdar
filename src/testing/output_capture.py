from contextlib import redirect_stdout
import io

class TestHelpers:
    def __generic_test_output_raw_capture(self, test_runner):
        f = io.StringIO()
        with redirect_stdout(f):
            test_runner()
        return f.getvalue()

    def get_motor_output(self, test_runner):
        test_output = self . __generic_test_output_raw_capture(test_runner)

        lines = test_output.split('\n')

        return_value = {}
        
        for line in lines:
            split_line = line . split()

            if len(split_line) < 12:
                continue

            if split_line[1] != 'motor':
                continue

            motor_port = split_line[3]

            exec_descriptor = {
                'speed': split_line[-3],
                'duration': split_line[-1][:-2]
            }
            
            if motor_port not in return_value:
                return_value[motor_port] = [exec_descriptor]
            else:
                return_value[motor_port].append(exec_descriptor)

        return return_value
