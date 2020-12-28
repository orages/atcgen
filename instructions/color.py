import logging
from itertools import chain

from new_generator.instruction import BaseInstruction
from new_generator.generator import TimEntry
from new_generator.event import EventComponentText
from new_generator.style import Style

from pyparsing import (Word, hexnums, Group, Optional)


COLORS_PARSER = ((
    Group(Word(hexnums, exact=2).leaveWhitespace() * 4
          ) | Group(Word(hexnums, exact=2).leaveWhitespace() * 3)
) + Optional('')) * 3

_LOGGER = logging.getLogger(__name__)


class ColorInstruction(BaseInstruction):
    """docstring for CreditInstructions"""

    def __init__(self):
        super(BaseInstruction, self).__init__()

    @staticmethod
    def set_up(context):
        pass

    def parse(self, args_str):
        parsed_args = COLORS_PARSER.parseString(args_str, parseAll=True)
        return parsed_args

    def process(self, full_line, args_str, context):
        parsed_args = self.parse(args_str)
        color_before = parsed_args[0]
        color_during = parsed_args[1]
        color_after = parsed_args[2]

        color_before_str = self.color_component_list_to_str(color_before)
        color_during_str = self.color_component_list_to_str(color_during)
        color_after_str = self.color_component_list_to_str(color_after)

        style_name_base = "Default"
        style_number = 1 # increment while names collides
        style_name = style_name_base
        while style_name in context["styles"]["available"]:
            style_name = style_name_base + str(style_number)
            style_number += 1

        new_style = Style(
            Name=style_name,
            SecondaryColour=color_before_str,
            KaraokeColour=color_during_str,
            PrimaryColour=color_after_str,
        )
        context["styles"]["available"][style_name] = new_style
        context["styles"]["active"] = style_name

    def color_component_list_to_str(self, color_component_list):
        str_parts = ["&H"]
        if len(color_component_list) == 3:
            str_parts.append("00")
        return ''.join(chain(str_parts, color_component_list[::-1]))


INSTRUCTIONS = {
    "color": ColorInstruction,
    "colors": ColorInstruction,
}
