# common utilities for all report languages
# this script will be sourced by al report_*.py language scripts.

def init_common(
        _on_port_fstr,
        _input_bool_prompt_ext,
        _input_bool_possibilities,
        _input_bool_no,
        _input_bool_err_msg,
        _input_int_err_msg):
    global _g_on_port_fstr
    global _g_input_bool_prompt_ext
    global _g_input_bool_possibilities
    global _g_input_bool_no
    global _g_input_bool_err_msg
    global _g_input_int_err_msg
    _g_on_port_fstr = _on_port_fstr
    _g_input_bool_prompt_ext = _input_bool_prompt_ext
    _g_input_bool_possibilities = _input_bool_possibilities
    _g_input_bool_no = _input_bool_no
    _g_input_bool_err_msg = _input_bool_err_msg
    _g_input_int_err_msg = _input_int_err_msg

def on_port(port):
    if port == None:
        return ''
    return _g_on_port_fstr.format(port)

def debug(msg, value=None, value2=None):
    # set to True to enable debug info
    if False:
        if value == None:
            print(' ', msg)
        elif value2 == None:
            print(' ', msg + ':', value)
        else:
            print(' ', msg + ':', str(value) + ':', value2)

def input_bool(prompt):
    """
    Get a bool from the user.
    """
    prompt += _g_input_bool_prompt_ext
    inp = input(prompt).strip()
    while len(inp) == 0 or (not inp[0].upper() in _g_input_bool_possibilities):
        print(_g_input_bool_err_msg)
        inp = input(prompt).strip()
    return inp[0].upper() != _g_input_bool_no

def input_int(prompt):
    """
    Get an int from the user.
    """
    prompt += ' '
    inp = input(prompt).strip()
    while not inp.isnumeric():
        print(_g_input_int_err_msg)
        inp = input(prompt).strip()
    return int(inp)

def leds(group):
    for l in group:
        led(l)
