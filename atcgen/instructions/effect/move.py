from atcgen.instructions.effect import Effect
from atcgen.event import EventComponentEffect

from pyparsing import (Combine, Optional, Word, alphanums, nums, tokenMap)
from distutils.util import strtobool


def INTEGER(name):
    """generate INTEGER parser"""
    return Combine(Optional('-') + Word(nums)).setParseAction(
        tokenMap(int)).setName(name)


MOVE_ARGS_PARSER = Word(alphanums) + INTEGER("x_start") + INTEGER(
    "y_start") + INTEGER("x_end") + INTEGER("y_end")


class EventComponentEffectMove(EventComponentEffect):

    def __init__(self, *args, **kwargs):
        super(EventComponentEffectMove, self).__init__(*args, **kwargs)
        self.x = 0
        self.y = 0
        self.rendering_helpers["tass"] = self._render_tass

    def set_move(self, x_start, y_start, x_end, y_end):
        self.x_start = x_start
        self.y_start = y_start
        self.x_end = x_end
        self.y_end = y_end

    def _render_tass(self, event, escape_fn=None):
        return ("{{\\move({x_start}, {y_start}, {x_end}, {y_end})}}".format(
                x_start=self.x_start, y_start=self.y_start,
                x_end=self.x_end, y_end=self.y_end,
                ))


class MoveEffect(Effect):

    def __init__(self):
        super(MoveEffect, self).__init__()
        self.full_line = ''
        self.args_str = ''

    @staticmethod
    def help(context):
        return (
            "Move an event text across the screen.\n\n"

            "arguments: STATUS X_START Y_START X_END Y_END\n\n"

            "+-----------------+-----------------+-------------------------+\n"
            "| argument name   | argument type   | description             |\n"
            "+=================+=================+=========================+\n"
            "| STATUS          | text            | 'y', 'yes', 't',        |\n"
            "|                 |                 | 'true',                 |\n"
            "|                 |                 | 'on' or '1' to enable   |\n"
            "|                 |                 | the effect, 'n', 'no',  |\n"
            "|                 |                 | 'f', 'false', 'off',    |\n"
            "|                 |                 | or '0' to disable it.   |\n"
            "+-----------------+-----------------+-------------------------+\n"
            "| X_START         | integer         | X coordinate at the     |\n"
            "|                 |                 | beginning               |\n"
            "+-----------------+-----------------+-------------------------+\n"
            "| Y_START         | integer         | Y coordinate at the     |\n"
            "|                 |                 | beginning               |\n"
            "+-----------------+-----------------+-------------------------+\n"
            "| X_END           | integer         | X coordinate at the     |\n"
            "|                 |                 | end                     |\n"
            "+-----------------+-----------------+-------------------------+\n"
            "| Y_END           | integer         | Y coordinate at the     |\n"
            "|                 |                 | end                     |\n"
            "+-----------------+-----------------+-------------------------+\n"
            '\n'


            "(x=0 ; y=0) correspond to the top left corner.\n"
            "Reference coordinate of the text depends on its Alignment.\n\n"

            "Examples:\n\n"
            "::\n\n"
            "    # move event from top left to bottom right\n"
            "    %effect move on 0 0 1280 720\n"
        )

    def parse(self, args_str):
        parsed_args = MOVE_ARGS_PARSER.parseString(self.args_str,
                                                   parseAll=True)
        return parsed_args

    def process(self, full_line, args_str, context):
        self.full_line = full_line
        self.args_str = args_str
        parsed_args = self.parse(self.args_str)
        values = {
            "active": strtobool(parsed_args[0]),
            'x_start': parsed_args[1],
            'y_start': parsed_args[2],
            'x_end': parsed_args[3],
            'y_end': parsed_args[4],
        }
        context["effects"]["move"] = values

    @staticmethod
    def set_up(context):
        context["effects"]["move"] = {
            "active": 0,
            'x_start': 0,
            'y_start': 0,
            'x_end': 0,
            'y_end': 0,
        }
        context["hooks"]["event.post_complete"].append(
            MoveEffect.event_post_complete_hook
        )

    @staticmethod
    def event_post_complete_hook(context, event):
        active = context["effects"]["move"]["active"]
        if not active:
            return
        x_start = context["effects"]["move"]['x_start']
        y_start = context["effects"]["move"]['y_start']
        x_end = context["effects"]["move"]['x_end']
        y_end = context["effects"]["move"]['y_end']
        move_component = EventComponentEffectMove('', None, context)
        move_component.set_move(x_start, y_start, x_end, y_end)
        event.components.insert(0, move_component)


EFFECTS = {"move": MoveEffect}
