import ev3dev.ev3 as ev3

def light_led(led, color):
    ev3.Leds.set_color(led, color)

def light_left(rcv):
    if (rcv == 1):
        light_led(ev3.Leds.LEFT, ev3.Leds.GREEN)
    else:
        light_led(ev3.Leds.LEFT, ev3.Leds.RED)

def light_right(rcv):
    if (rcv == 1):
        light_led(ev3.Leds.RIGHT, ev3.Leds.GREEN)
    else:
        light_led(ev3.Leds.RIGHT, ev3.Leds.RED)
