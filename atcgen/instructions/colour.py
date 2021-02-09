import logging
from itertools import chain

from atcgen.instruction import BaseInstruction
from atcgen.generator import TimEntry
from atcgen.event import EventComponentText
from atcgen.style import Style

from pyparsing import (Word, hexnums, Group, Optional, Empty)


colourS_PARSER = ((
    Group(Word(hexnums, exact=2).leaveWhitespace() * 4
          ) | Group(Word(hexnums, exact=2).leaveWhitespace() * 3)
) + Optional(Empty())) * 3

_LOGGER = logging.getLogger(__name__)


class ColourInstruction(BaseInstruction):
    """docstring for CreditInstructions"""

    def __init__(self):
        super(BaseInstruction, self).__init__()

    @staticmethod
    def help(context):
        return (
            "Simple style declaration.\n\n"

            "arguments: COLOUR_BEFORE COLOUR_DURING, COLOUR_AFTER\n\n"


            "+-----------------+-----------------+-------------------------+\n"
            "| argument name   | argument type   | description             |\n"
            "+=================+=================+=========================+\n"
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

            "Generated styles are named \"Default#\" where # is replaced "
            "by an increasing number to avoid collisions (starting at 1).\n\n"

            "Examples:\n\n"
            "::\n\n"
            "    # declare a style with colours RED => GREEN => BLUE\n"
            "    %colour FF0000 00FF00 0000FF\n"
        )

    @staticmethod
    def set_up(context):
        pass

    def parse(self, args_str):
        parsed_args = colourS_PARSER.parseString(args_str, parseAll=True)
        return parsed_args

    def process(self, full_line, args_str, context):
        parsed_args = self.parse(args_str)
        colour_before = parsed_args[0]
        colour_during = parsed_args[1]
        colour_after = parsed_args[2]

        colour_before_str = self.colour_component_list_to_str(colour_before)
        colour_during_str = self.colour_component_list_to_str(colour_during)
        colour_after_str = self.colour_component_list_to_str(colour_after)

        style_name_base = "Default"
        style_number = 1  # increment while names collides
        style_name = style_name_base
        while style_name in context["styles"]["available"]:
            style_name = style_name_base + str(style_number)
            style_number += 1

        new_style = Style(
            Name=style_name,
            SecondaryColour=colour_before_str,
            KaraokeColour=colour_during_str,
            PrimaryColour=colour_after_str,
        )
        context["styles"]["available"][style_name] = new_style
        context["styles"]["active"] = style_name

    def colour_component_list_to_str(self, colour_component_list):
        str_parts = ["&H"]
        if len(colour_component_list) == 3:
            str_parts.append("00")
        return ''.join(chain(str_parts, colour_component_list[::-1]))


INSTRUCTIONS = {
    "colour": ColourInstruction,
    "colours": ColourInstruction,
    "color": ColourInstruction,
    "colors": ColourInstruction,
}
