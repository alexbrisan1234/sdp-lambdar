# This script provides procedures to output stati and changes
# concerning the pseudo-ev3 test to the user.

from ev3dev.report_common import *

init_common(
    _input_bool_prompt_ext = ' [yes/no] ',
    _input_bool_possibilities = 'YN',
    _input_bool_no = 'N',
    _input_bool_err_msg = 'Please input yes or no!',
    _input_int_err_msg = 'Please input an integer!',
    _on_port_fstr = ' on {0}')

# Motor
def motor_start(port, speed):
    print('The motor'
          + on_port(port)
          + ' is rotating with the speed {0}.'.format(speed))
def motor_running_timed(port, speed, time):
    print('The motor'
          + on_port(port)
          + ' is rotating with the speed {0} for {1}s.'.format(speed, time/1000))
def motor_stopped(port, brake):
    print('The motor'
          + on_port(port)
          + (' brakes.' if brake else ' stops.'))

# Led
def led_side(led):
    name_pattern = led.get_attr_string(None, 'name_pattern')[1]
    if 'left' in name_pattern:
        return 'left'
    elif 'right' in name_pattern:
        return 'right'
    return 'unknown'
def led_color(led):
    name_pattern = led.get_attr_string(None, 'name_pattern')[1]
    if 'red' in name_pattern:
        return 'red'
    elif 'green' in name_pattern:
        return 'green'
    return 'unknown colored'
def led(led):
    side = led_side(led)
    color = led_color(led)
    brightness = led.brightness_pct
    print('The {0} {1} LED'.format(side, color)
          + (' is now off.' if brightness == 0
             else ' is now on with a brightness of {0}.'.format(brightness)))

# Sound
def sound_beep(args):
    print('beep {0}'.format(args))
def sound_play(path):
    print('{0} is playing.'.format(path))
def sound_speak(text):
    print('The EV3 says: "{0}"'.format(text))
def sound_set_volume(volume):
    print('The volume is now {0}%.'.format(volume * 100))

# Sensors
# Touch Sensor
def sensor_touch(port):
    return input_bool('Is the touch sensor'
                      + on_port(port)
                      + ' pressed?')
# Color Sensor
def sensor_color_ambient(port):
    return input_int('How bright is it at the color sensor'
                     + on_port(port)
                     + ' in %?') / 100
def sensor_color_reflect(port):
    return input_int('How much light gets reflected at the color sensor'
                     + on_port(port)
                     + ' in %?') / 100
def sensor_color_color(port):
    return input_int('Which color is at the color sensor'
                     + on_port(port)
                     + """?
          - 0: None
          - 1: black
          - 2: blue
          - 3: green
          - 4: yellow
          - 5: red
          - 6: white
          - 7: brown
          """)
def sonsor_color_raw_reflect(port):
    return input_int('How much light gets reflected at the color sensor'
                     + on_port(port)
                     + '?')
def sensor_color_raw_color(port, color):
    colors = ('red', 'green', 'blue')
    return input_int('How much {0} light gets reflected at the color sensor'
                     .format(colors[color])
                     + on_port(port)
                     + '?')

# Ultrasonic Sensor
def sensor_ultrasonic_dist(port):
    return input_int('How many cm are in front of the ultrasonic sensor'
                     + on_port(port)
                     + '?')
def sensor_ultrasonic_nearby(port):
    return input_bool('Is there an other ultrasonis sensor near the one'
                      + on_port(port)
                      + '?')

# Gyroscope
def sensor_gyro_angle(port):
    return input_int('By how many degrees was the gyroscope'
                     + on_port(port)
                     + ' already turned?')
def sensor_gyro_rate(port):
    return input_int('By how many degrees per seconde does the gyroscope'
                     + on_port(port)
                     + ' turn?')

# Infrared Sensor
def sensor_infrared_prox(port):
    return input_int('How many cm is the infrared sensor'
                     + on_port(port)
                     + ' away from the remote?') / 70

# Sound Sensors
def sensor_sound(port):
    return input_int('How strong is the soundpreassure at the sound sensor'
                     + on_port(port)
                     + '?')
# Light Sensor
def sensor_light_ambient(port):
    return input_int('How bright is it at the light sensor'
                     + on_port(port)
                     + '?')
def sensor_light_reflect(port):
    return input_int('How much light gets reflected at the light sensor'
                     + on_port(port)
                     + '?')


# Power
def power_current():
    return input_int('How high is the current??')
def power_voltage():
    return input_int('How high is the voltage?')
def power_voltage_min():
    return input_int('How high is the min voltage?')
def power_voltage_max():
    return input_int('How high is the max voltage?')
