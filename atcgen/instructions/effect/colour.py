from itertools import chain

from atcgen.instructions.effect import Effect
from atcgen.event import EventComponentEffect

from pyparsing import (Empty, Group, Optional, Word,
                       alphanums, hexnums, tokenMap)
from distutils.util import strtobool


COLOURS_PARSER = Word(alphanums).setParseAction(
    tokenMap(strtobool)).setName("toggle") + Optional(((
        Group(Word(hexnums, exact=2).leaveWhitespace() * 4
              ) | Group(Word(hexnums, exact=2).leaveWhitespace() * 3)
    ) + Optional(Empty())) * 3)


class EventComponentEffectColour(EventComponentEffect):

    def __init__(self, *args, **kwargs):
        super(EventComponentEffectColour, self).__init__(*args, **kwargs)
        self.status = None
        self.colour_before = None
        self.colour_during = None
        self.colour_after = None
        self.rendering_helpers["tass"] = self._render_tass

    def set_colours(self, colour_before, colour_during, colour_after):
        self.colour_before = colour_before
        self.colour_during = colour_during
        self.colour_after = colour_after

    def _render_tass(self, event, escape_fn=None):
        return ("{{\\2c({before})\\5c({during})\\1c({after})}}".format(
                before=self.colour_before,
                during=self.colour_during,
                after=self.colour_after,
                ))


class ColourEffect(Effect):

    def __init__(self):
        super(ColourEffect, self).__init__()
        self.full_line = ''
        self.args_str = ''

    @staticmethod
    def help(context):
        return (
            "Change text color inside an event.\n\n"

            "arguments: STATUS COLOUR_BEFORE COLOUR_DURING COLOUR_AFTER\n\n"

            "+-----------------+-----------------+-------------------------+\n"
            "| argument name   | argument type   | description             |\n"
            "+=================+=================+=========================+\n"
            "| STATUS          | text            | 'y', 'yes', 't', 'true',|\n"
            "|                 |                 | 'on' or '1' to enable   |\n"
            "|                 |                 | the effect, 'n', 'no',  |\n"
            "|                 |                 | 'f', 'false', 'off',    |\n"
            "|                 |                 | or '0' to disable it.   |\n"
            "+-----------------+-----------------+-------------------------+\n"
            "| COLOUR_BEFORE   | RGB or RGBA     | SecondaryColour         |\n"
            "|                 | hexadecimal     |                         |\n"
            "|                 | sequences       |                         |\n"
            "+-----------------+-----------------+-------------------------+\n"
            "| COLOUR_DURING   | RGB or RGBA     | KaraokeColour           |\n"
            "|                 | hexadecimal     |                         |\n"
            "|                 | sequences       |                         |\n"
            "+-----------------+-----------------+-------------------------+\n"
            "| COLOUR_AFTER    | RGB or RGBA     | PrimaryColour           |\n"
            "|                 | hexadecimal     |                         |\n"
            "|                 | sequences       |                         |\n"
            "+-----------------+-----------------+-------------------------+\n"
            '\n'

            "Status can be used to stop the effect from changing the\n"
            "next events.\n"
            "To cancel in the middle of an event, use the \"reset\" effect.\n"
            '\n'

            "Examples:\n\n"
            "::\n\n"
            "    # set color_before as red for the word \"akai\" only\n"
            "    %colour 00FFFF 00FF00 FF0000\n"
            "    &IN &MY &DREAM \\\n"
            "    %effect colour on 0000FF 00FF00 FF0000\n"
            "    &a&ka&i \\\n"
            "    %effect reset\n"
            "    %effect colour off\n"
            "    &ba&ra &no &ha&na\n"
        )

    def parse(self, args_str):
        parsed_args = COLOURS_PARSER.parseString(self.args_str,
                                                 parseAll=True)
        return parsed_args

    def process(self, full_line, args_str, context):
        self.full_line = full_line
        self.args_str = args_str
        parsed_args = self.parse(self.args_str)
        values = {
            "active_on_events": set(),
            "status": parsed_args[0],
            'before': self.colour_component_list_to_str(parsed_args[1]),
            'during': self.colour_component_list_to_str(parsed_args[2]),
            'after': self.colour_component_list_to_str(parsed_args[3]),
        }
        context["effects"]["colour"] = values
        event = context["events"]["current"]
        if event is not None:
            colour_component = EventComponentEffectColour('', None, context)
            colour_component.set_colours(
                values["before"],
                values["during"],
                values["after"])
            event.components.append(colour_component)

    @staticmethod
    def set_up(context):
        context["effects"]["colour"] = {
            "status": False,
            "before": None,
            "during": None,
            "after": None,
        }
        context["hooks"]["event.post_create"].append(
            ColourEffect.event_post_create_hook
        )

    @staticmethod
    def event_post_create_hook(context, event):
        active = context["effects"]["colour"]["status"]
        if not active:
            return
        values = context["effects"]["colour"]
        colour_component = EventComponentEffectColour('', None, context)
        colour_component.set_colours(
            values["before"],
            values["during"],
            values["after"])
        event.components.append(colour_component)

    def colour_component_list_to_str(self, colour_component_list):
        str_parts = ["&H"]
        if len(colour_component_list) == 3:
            str_parts.append("00")
        return ''.join(chain(str_parts, colour_component_list[::-1]))


EFFECTS = {
    "color": ColourEffect,
    "colour": ColourEffect,
    "colors": ColourEffect,
    "colours": ColourEffect,
}
