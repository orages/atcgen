from new_generator.instructions.effect import Effect
from new_generator.event import EventComponentEffect

from pyparsing import (Combine, Optional, Word, alphanums, nums, tokenMap)
from distutils.util import strtobool


def INTEGER(name):
    """generate INTEGER parser"""
    return Combine(Optional('-') + Word(nums)).setParseAction(
        tokenMap(int)).setName(name)


POSITION_ARGS_PARSER = Word(alphanums) + INTEGER("x") + INTEGER("y")


class EventComponentEffectPosition(EventComponentEffect):

    def __init__(self, *args, **kwargs):
        super(EventComponentEffectPosition, self).__init__(*args, **kwargs)
        self.x = 0
        self.y = 0
        self.rendering_helpers["tass"] = self._render_tass

    def set_position(self, x, y):
        self.x = x
        self.y = y

    def _render_tass(self, event, escape_fn=None):
        return ("{{\\pos({x}, {y})}}".format(
                x=self.x,
                y=self.y))


class PositionEffect(Effect):

    def __init__(self):
        super(PositionEffect, self).__init__()
        self.full_line = ''
        self.args_str = ''

    @staticmethod
    def help(context):
        return (
            "Force event text position on the screen.\n\n"

            "arguments: STATUS X Y\n\n"

            "+---------------+---------------+-----------------------------+\n"
            "| argument name | argument type | description                 |\n"
            "+===============+===============+=============================+\n"
            "| STATUS        | text          | 'y', 'yes', 't', 'true',    |\n"
            "|               |               | 'on' or '1' to enable       |\n"
            "|               |               | the effect, 'n', 'no',      |\n"
            "|               |               | 'f', 'false', 'off',        |\n"
            "|               |               | or '0' to disable it.       |\n"
            "+---------------+---------------+-----------------------------+\n"
            "| X             | integer       | X coordinate                |\n"
            "+---------------+---------------+-----------------------------+\n"
            "| Y             | integer       | Y coordinate                |\n"
            "+---------------+---------------+-----------------------------+\n"
            '\n'


            "(x=0 ; y=0) correspond to the top left corner.\n"
            "Reference coordinate of the text depends on its Alignment.\n\n"

            "Examples:\n\n"
            "::\n\n"
            "    # display text at 190 110\n"
            "    %effect position on 190 110\n"
        )

    def parse(self, args_str):
        parsed_args = POSITION_ARGS_PARSER.parseString(self.args_str,
                                                       parseAll=True)
        return parsed_args

    def process(self, full_line, args_str, context):
        self.full_line = full_line
        self.args_str = args_str
        parsed_args = self.parse(self.args_str)
        values = {
            "active": strtobool(parsed_args[0]),
            'x': parsed_args[1],
            'y': parsed_args[2],
        }
        context["effects"]["position"] = values

    @staticmethod
    def set_up(context):
        context["effects"]["position"] = {
            "active": 0,
            'x': 0,
            'y': 0,
        }
        context["hooks"]["event.post_complete"].append(
            PositionEffect.event_post_complete_hook
        )

    @staticmethod
    def event_post_complete_hook(context, event):
        active = context["effects"]["position"]["active"]
        if not active:
            return
        x = context["effects"]["position"]['x']
        y = context["effects"]["position"]['y']
        position_component = EventComponentEffectPosition('', None, context)
        position_component.set_position(x, y)
        event.components.insert(0, position_component)


EFFECTS = {"position": PositionEffect}
