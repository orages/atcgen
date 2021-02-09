class Style(object):

    __slots__ = (
        "__weakref__",
        "Name",
        "Fontname",
        "Fontsize",
        "PrimaryColour",
        "SecondaryColour",
        "KaraokeColour",
        "OutlineColour",
        "BackColour",
        "Bold",
        "Italic",
        "Underline",
        "StrikeOut",
        "ScaleX",
        "ScaleY",
        "Spacing",
        "Angle",
        "BorderStyle",
        "Outline",
        "Shadow",
        "Alignment",
        "MarginL",
        "MarginR",
        "MarginV",
        "Encoding",
        "locked",        # lock the instance after init
        "extra_data",    # unused dict
                         # available for instructions and effect developers
    )

    def __init__(self, Name="Default", Fontname="DejaVu Sans", Fontsize=25,
                 PrimaryColour="&H0000FF00", SecondaryColour="&H0000FFFF",
                 KaraokeColour="&H000000FF", OutlineColour="&H00000000",
                 BackColour="&H00000000", Bold=0, Italic=0, Underline=0,
                 StrikeOut=0, ScaleX=200, ScaleY=200, Spacing=0, Angle=0,
                 BorderStyle=1, Outline=5, Shadow=2, Alignment=8, MarginL=10,
                 MarginR=10, MarginV=10, Encoding=1):
        self.locked = False  # prevent raising useless exceptions
        self.extra_data = {}
        self.Name = Name
        self.Fontname = Fontname
        self.Fontsize = Fontsize
        self.PrimaryColour = PrimaryColour
        self.SecondaryColour = SecondaryColour
        self.KaraokeColour = KaraokeColour
        self.OutlineColour = OutlineColour
        self.BackColour = BackColour
        self.Bold = Bold
        self.Italic = Italic
        self.Underline = Underline
        self.StrikeOut = StrikeOut
        self.ScaleX = ScaleX
        self.ScaleY = ScaleY
        self.Spacing = Spacing
        self.Angle = Angle
        self.BorderStyle = BorderStyle
        self.Outline = Outline
        self.Shadow = Shadow
        self.Alignment = Alignment
        self.MarginL = MarginL
        self.MarginR = MarginR
        self.MarginV = MarginV
        self.Encoding = Encoding
        self.locked = True

    def __setattr__(self, attribute, value):
        try:
            if self.locked:
                raise AttributeError("Style is read-only.")
        except AttributeError:
            pass
        super().__setattr__(attribute, value)

    def format(self, formatter):
        return formatter.format(**self.to_dict())

    def to_dict(self):
        return {
            "Name": self.Name,
            "Fontname": self.Fontname,
            "Fontsize": self.Fontsize,
            "PrimaryColour": self.PrimaryColour,
            "SecondaryColour": self.SecondaryColour,
            "KaraokeColour": self.KaraokeColour,
            "OutlineColour": self.OutlineColour,
            "BackColour": self.BackColour,
            "Bold": self.Bold,
            "Italic": self.Italic,
            "Underline": self.Underline,
            "StrikeOut": self.StrikeOut,
            "ScaleX": self.ScaleX,
            "ScaleY": self.ScaleY,
            "Spacing": self.Spacing,
            "Angle": self.Angle,
            "BorderStyle": self.BorderStyle,
            "Outline": self.Outline,
            "Shadow": self.Shadow,
            "Alignment": self.Alignment,
            "MarginL": self.MarginL,
            "MarginR": self.MarginR,
            "MarginV": self.MarginV,
            "Encoding": self.Encoding,
            "extra_data": self.extra_data,
            "locked": self.locked,
        }
