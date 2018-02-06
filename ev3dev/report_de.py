# This script provides procedures and strings to output stati and
# changes concerning the pseudo-ev3 test to the user. It will be
# sourced by report.py

from ev3dev.report_common import *

init_common(
    _input_bool_prompt_ext = ' [Ja/Nein] ',
    _input_bool_possibilities = 'JN',
    _input_bool_no = 'N',
    _input_bool_err_msg = 'Bitte gebe Ja oder Nein ein!',
    _input_int_err_msg = 'Bitte gebe eine Ganzzahl ein!',
    _on_port_fstr = ' an {0}')

# Motor
def motor_start(port, speed):
    print('Der Motor'
          + on_port(port)
          + ' dreht sich mit der Geschwindigkeit {0}.'.format(speed))
def motor_running_timed(port, speed, time):
    print('Der Motor'
          + on_port(port)
          + ' dreht sich mit der Geschwindigkeit {0} für {1}s.'
          .format(speed, time/1000))
def motor_stopped(port, brake):
    print('Der Motor'
          + on_port(port)
          + (' bremst.' if brake else ' stoppt.'))

# Led
def led_side(led):
    name_pattern = led.get_attr_string(None, 'name_pattern')[1]
    if 'left' in name_pattern:
        return 'linke'
    elif 'right' in name_pattern:
        return 'rechte'
    return 'unbekannte'
def led_color(led):
    name_pattern = led.get_attr_string(None, 'name_pattern')[1]
    if 'red' in name_pattern:
        return 'rote'
    elif 'green' in name_pattern:
        return 'grüne'
    return 'unbekannt gefärbte'
def led(led):
    side = led_side(led)
    color = led_color(led)
    brightness = led.brightness_pct
    print('Die {0} {1} LED'.format(side, color)
          + (' ist nun aus.' if brightness == 0
             else ' leuchtet nun mit der Helligkeit {0}.'.format(brightness)))

# Sound
def sound_beep(args):
    print('beep {0}'.format(args))
def sound_play(path):
    print('{0} wird abgespielt.'.format(path))
def sound_speak(text):
    print('Der EV3 sagt: "{0}"'.format(text))
def sound_set_volume(volume):
    print('Die Lautstärke ist nun {0}%.'.format(volume * 100))

# Sensors
# Touch Sensor
def sensor_touch(port):
    return input_bool('Ist der Berührungssensor'
                      + on_port(port)
                      + ' gedrückt?')
# Color Sensor
def sensor_color_ambient(port):
    return input_int('Wie hell ist es an dem Farbsensor'
                     + on_port(port)
                     + ' in %?') / 100
def sensor_color_reflect(port):
    return input_int('Wie viel Licht wird bei dem Farbsensor'
                     + on_port(port)
                     + ' in % reflektiert?') / 100
def sensor_color_color(port):
    return input_int('Welche Farbe ist an dem Farbsensor'
                     + on_port(port)
                     + """?
          - 0: keine
          - 1: schwarz
          - 2: blau
          - 3: grün
          - 4: gelb
          - 5: rot
          - 6: weiß
          - 7: braun
          """)
def sonsor_color_raw_reflect(port):
    return input_int('Wie viel Licht wird an dem Farbsensor'
                     + on_port(port)
                     + ' reflektiert?')
def sensor_color_raw_color(port, color):
    colors = ('rotes', 'grünes', 'blaues')
    return input_int('Wie viel {0} Licht wird am Farbsensor'
                     .format(colors[color])
                     + on_port(port)
                     + 'reflektiert?')

# Ultrasonic Sensor
def sensor_ultrasonic_dist(port):
    return input_int('Wie viele cm sind vor dem Ultraschallsensor'
                     + on_port(port)
                     + 'frei?')
def sensor_ultrasonic_nearby(port):
    return input_bool('Ist ein Weiterer nahe dem Ultraschallsensor'
                      + on_port(port)
                      + '?')

# Gyroscope
def sensor_gyro_angle(port):
    return input_int('Um wie viele Grad wurde das Gyroskop'
                     + on_port(port)
                     + ' bereits gedreht?')
def sensor_gyro_rate(port):
    return input_int('Um wie viele Grad pro Sekunde dreht sich das Gyroskop'
                     + on_port(port)
                     + '?')

# Infrared Sensor
def sensor_infrared_prox(port):
    return input_int('Wie viele cm ist der Infrarotsensor'
                     + on_port(port)
                     + ' von der Fernbedienung entfernt?') / 70

# Sound Sensors
def sensor_sound(port):
    return input_int('Wie stark ist der Schalldruck am Schallsensor'
                     + on_port(port)
                     + '?')
# Light Sensor
def sensor_light_ambient(port):
    return input_int('Wie hell ist es am Lichtsensor'
                     + on_port(port)
                     + '?')
def sensor_light_reflect(port):
    return input_int('Wie viel Licht wird am Lichtsensor'
                     + on_port(port)
                     + 'reflektiert?')


# Power
def power_current():
    return input_int('Wie hoch ist die Stromstärke??')
def power_voltage():
    return input_int('Wie hoch ist die Spannung?')
def power_voltage_min():
    return input_int('Wie hoch ist die minimale Spannung?')
def power_voltage_max():
    return input_int('Wie hoch ist die maximale Spannung?')
