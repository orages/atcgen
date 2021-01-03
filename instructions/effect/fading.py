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

    @staticmethod
    def help(context):
        return (
            "Add a fade in and fade out effect to the events.\n\n"

            "Active by default with preset:\n"
            "  - fade in duration: 750ms\n"
            "  - fade out duration: 500ms\n"
            "  - fade in delay: -100cs\n"
            "  - fade out delay: 50cs\n\n"

            "arguments: FADEIN_DURATION FADEOUT_DURATION "
            "FADEIN_DELAY FADEOUT_DELAY\n\n"

            "+------------------+-----------------+------------------------+\n"
            "| argument name    | argument type   | description            |\n"
            "+==================+=================+========================+\n"
            "| FADEIN_DURATION  | integer (in ms) | Duration of the fade   |\n"
            "|                  |                 | in effect              |\n"
            "+------------------+-----------------+------------------------+\n"
            "| FADEOUT_DURATION | integer (in ms) | Duration of the fade   |\n"
            "|                  |                 | in effect              |\n"
            "+------------------+-----------------+------------------------+\n"
            "| FADEIN_DELAY     | integer (in ms) | Shift the beginning    |\n"
            "|                  |                 | of the event to avoid  |\n"
            "|                  |                 | overlapping fading     |\n"
            "|                  |                 | effect and sung        |\n"
            "|                  |                 | syllables.             |\n"
            "+------------------+-----------------+------------------------+\n"
            "| FADEOUT_DELAY    | integer (in ms) | Shift the end of       |\n"
            "|                  |                 | the event to avoid     |\n"
            "|                  |                 | overlapping fading     |\n"
            "|                  |                 | effect and             |\n"
            "|                  |                 | sung syllables.        |\n"
            "+------------------+-----------------+------------------------+\n"
            '\n'

            "If the cursor is disabled or (re-enabled) in the middle of an "
            "event, place-holder components are inserted to avoid "
            "misalignment of syllables.\n\n"

            "Examples:\n\n"
            "::\n\n"
            "    # at apparition text fade in for 0.75s\n"
            "    # then stays still for 0.25s\n"
            "    # then is sung\n"
            "    # then disappear in a fade out during 0.5s\n"
            "    %effect passing 750 500 -100 50\n"
        )

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
