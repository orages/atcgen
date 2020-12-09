from new_generator.instructions.effect import Effect
from new_generator.event import EventComponentEffect

from pyparsing import (Combine, Optional, Word, nums, tokenMap)


def INTEGER(name):
    """generate INTEGER parser"""
    return Combine(Optional('-') + Word(nums)).setParseAction(
        tokenMap(int)).setName(name)


FADING_ARGS_PARSER = INTEGER(
    "fadein_duration") + INTEGER("fadeout_duration") + INTEGER(
    "fadein_delay") + INTEGER("fadeout_delay")


class EventComponentEffectFading(EventComponentEffect):

    def __init__(self, *args, **kwargs):
        super(EventComponentEffectFading, self).__init__(*args, **kwargs)
        self.fadein_duration = 0
        self.fadeout_duration = 0
        self.rendering_helpers["tass"] = self._render_tass

    def set_fading(self, fadein_duration, fadeout_duration):
        self.fadein_duration = fadein_duration
        self.fadeout_duration = fadeout_duration

    def _render_tass(self, event, escape_fn=None):
        return ("{{\\fade({fadein_duration}, {fadeout_duration})}}".format(
                fadein_duration=self.fadein_duration,
                fadeout_duration=self.fadeout_duration))


class FadingEffect(Effect):

    def __init__(self):
        super(FadingEffect, self).__init__()
        self.full_line = ''
        self.args_str = ''

    def parse(self, args_str):
        parsed_args = FADING_ARGS_PARSER.parseString(self.args_str,
                                                     parseAll=True)
        return parsed_args

    def process(self, full_line, args_str, context):
        self.full_line = full_line
        self.args_str = args_str
        parsed_args = self.parse(self.args_str)
        values = {
            "fadein_duration": parsed_args[0],
            "fadeout_duration": parsed_args[1],
            "fadein_delay": parsed_args[2],
            "fadeout_delay": parsed_args[3],
        }
        context["effects"]["fading"] = values

    @staticmethod
    def set_up(context):
        context["effects"]["fading"] = {
            "fadein_duration": 750,
            "fadeout_duration": 500,
            "fadein_delay": -100,
            "fadeout_delay": 50,
        }
        context["hooks"]["event.post_complete"].append(
            FadingEffect.event_post_complete_hook
        )

    @staticmethod
    def event_post_complete_hook(context, event):

        fadein_duration = context["effects"]["fading"]["fadein_duration"]
        fadeout_duration = context["effects"]["fading"]["fadeout_duration"]
        fadein_delay = context["effects"]["fading"]["fadein_delay"]
        fadeout_delay = context["effects"]["fading"]["fadeout_delay"]
        event.start_timestamp += fadein_delay
        if event.start_timestamp < 0:
            event.start_timestamp = 0
        event.end_timestamp += fadeout_delay
        fading_component = EventComponentEffectFading('', None, context)
        fading_component.set_fading(fadein_duration, fadeout_duration)
        event.components.insert(0, fading_component)


EFFECTS = {"fading": FadingEffect}
