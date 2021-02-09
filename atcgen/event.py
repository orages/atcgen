import math

class EventComponent():

    def __init__(self, text='', tim_entry=None, context=None):
        self.text = text
        self.times = None
        if tim_entry is not None:
            self.times = tim_entry.times
        self.extra_data = {}
        self.rendering_helpers = {}

    def __repr__(self):
        return "<{class_name}: ({times}) {text_repr}>".format(
            class_name=self.__class__.__name__,
            times=self.times,
            text_repr=repr(self.text),
        )

    def get_begining_timestamp(self):
        if self.times is None:
            return None
        return self.times[0]

    def get_ending_timestamp(self):
        if self.times is None:
            return None
        return self.times[1]


class EventComponentEffect(EventComponent):
    pass


class EventComponentKaraokeSyllable(EventComponent):

    def __init__(self, text='', tim_entry=None, context=None):
        super(EventComponentKaraokeSyllable, self).__init__(
            text=text, tim_entry=tim_entry, context=context)
        self.karaoke_type = "kt"
        if context:
            self.karaoke_type = context.get("effects", {}).get(
                "karaoke_type", "kt")
        self.rendering_helpers["tass"] = self._render_tass

    def _render_tass(self, event, escape_fn=None):
        event_start = event.start_timestamp
        start_offset = self.get_begining_timestamp() - event_start
        duration = self.get_ending_timestamp() - self.get_begining_timestamp()
        text = self.text
        if escape_fn is not None:
            text = escape_fn(text)
        return (
            "{{\\{karaoke_type}({start_offset}, {duration})}}{text}".format(
                karaoke_type=self.karaoke_type, start_offset=start_offset,
                duration=duration, text=text))


class EventComponentText(EventComponent):

    def __init__(self, text='', tim_entry=None, context=None):
        super(EventComponentText, self).__init__(
            text=text, tim_entry=tim_entry, context=context)
        self.rendering_helpers["tass"] = self._render_tass

    def _render_tass(self, event, escape_fn=None):
        text = self.text
        if escape_fn is not None:
            text = escape_fn(text)
        return ("{text}".format(text=text))


class EventEffect(object):

    def __init__(self):
        super(EventEffect, self).__init__()
        self.name = ''
        self.args = ()
        self.rendering_helpers = {}


class Event(object):

    def __init__(self):
        self.components = []
        self.Type = "Dialogue"
        self.Layer = 0
        self.start_timestamp = None
        self.end_timestamp = None
        self.Style = None
        self.Name = ''
        self.MarginL = 0
        self.MarginR = 0
        self.MarginV = 0
        self.Effect = None
        self.extra_data = {}

    def complete(self, context):
        start = math.inf
        end = 0
        for compo in self.components:
            compo_begin = compo.get_begining_timestamp()
            compo_end = compo.get_ending_timestamp()
            if compo_begin:
                start = start if start < compo_begin else compo_begin
            if compo_end:
                end = end if end > compo_end else compo_end
        start = 0 if start == math.inf else start
        self.start_timestamp = start
        self.end_timestamp = end

    def to_dict(self):
        return {
            "components": self.components,
            "Type": self.Type,
            "Layer": self.Layer,
            "start_timestamp": self.start_timestamp,
            "end_timestamp": self.end_timestamp,
            "Style": self.Style,
            "Name": self.Name,
            "MarginL": self.MarginL,
            "MarginR": self.MarginR,
            "MarginV": self.MarginV,
            "Effect": self.Effect,
            "extra_data": self.extra_data,
        }
