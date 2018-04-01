import ev3dev.ev3 as ev3

def light_led(led, color):
    ev3.Leds.set_color(led, color)

#color = 0 (red) / 1 (green)
def light_left(color):
    if (color == 0):
        light_led(ev3.Leds.LEFT, ev3.Leds.RED)
    else:
        light_led(ev3.Leds.LEFT, ev3.Leds.GREEN)

def light_right(color):
    if (color == 0):
        light_led(ev3.Leds.RIGHT, ev3.Leds.RED)
    else:
        light_led(ev3.Leds.RIGHT, ev3.Leds.GREEN)