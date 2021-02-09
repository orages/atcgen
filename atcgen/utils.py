class ExceptionShield(object):

    def __init__(self, to_silence='*', log_handler=None,
                 format="Silence {type_name}: {value}"):
        self.to_silence = to_silence
        self.log_handler = log_handler if log_handler is not None else print
        self.format = format

    def __enter__(self):
        return None

    def __exit__(self, type_, value, traceback):
        handled = False
        if (type_, value, traceback) == (None, None, None):
            return handled
        type_obj = type(type_) if type_ is None else type_
        if self.to_silence == '*' or type_ in self.to_silence:
            self.log_handler(self.format.format(type=type_,
                                                type_name=type_obj.__name__,
                                                value=value))
            handled = True
        return handled


def RGBtoABGR(string):
    a = b = g = r = "00"
    if len(string) == 8:
        r = string[:2]
        g = string[2:4]
        b = string[4:6]
        a = string[6:]
    elif len(string) == 6:
        r = string[:2]
        g = string[2:4]
        b = string[4:]
    else:
        raise RuntimeError("colour string should be of length 6 or 8.")
    return '{}{}{}{}'.format(a, b, g, r)


def RGBseqToABGRseq(iterable):
    return [RGBtoABGR(_) for _ in iterable]


def intToTime(ts):
    h, m = divmod(ts, 100 * 60 * 60)
    m, s = divmod(m, 100 * 60)
    s, c = divmod(s, 100)
    string = "{:>01}:{:>02}:{:>02}.{:>02}".format(h, m, s, c)
    return string
