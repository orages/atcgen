import logging
from new_generator.instruction import BaseInstruction
from new_generator.generator import TimEntry
from new_generator.event import EventComponentText
from new_generator.style import Style

from pyparsing import (Word, nums, tokenMap, restOfLine)


def UINTEGER(name):
    """generate UINTEGER parser"""
    return Word(nums).setParseAction(tokenMap(int)).setName(name)


CREDIT_PARSER = UINTEGER("begin") + UINTEGER("end") + restOfLine.setName("txt")

_LOGGER = logging.getLogger(__name__)


class CreditInstruction(BaseInstruction):
    """docstring for CreditInstructions"""

    def __init__(self):
        super(BaseInstruction, self).__init__()

    def set_up(context):
        if "Credit" not in context["styles"]["available"]:
            context["styles"]["available"]["Credit"] = Style(
                Name="Credit",
                Fontname="DejaVu Sans",
                Fontsize=25,
                PrimaryColour="&H0000FF00",
                SecondaryColour="&H0000FFFF",
                KaraokeColour="&H000000FF",
                OutlineColour="&H00000000",
                BackColour="&H00000000",
                Bold=0,
                Italic=0,
                Underline=0,
                StrikeOut=0,
                ScaleX=200,
                ScaleY=200,
                Spacing=0,
                Angle=0,
                BorderStyle=1,
                Outline=2,
                Shadow=2,
                Alignment=1,
                MarginL=10,
                MarginR=10,
                MarginV=10,
                Encoding=1
            )

    def parse(self, args_str):
        parsed_args = CREDIT_PARSER.parseString(args_str, parseAll=True)
        return parsed_args

    def process(self, full_line, args_str, context):
        parsed_args = self.parse(args_str)
        begin = parsed_args[0]
        end = parsed_args[1]
        text = parsed_args[2]

        event_class = context["events"]["event_class"]
        fading_effect_available = False
        fading_component_class = None
        event = event_class()

        # check fading effect availability
        try:
            from new_generator.instructions.effect.fading import (
                EventComponentEffectFading)
            fading_component_class = EventComponentEffectFading
            fading_effect_available = True
        except ImportError:
            _LOGGER.warning("'fading' effect not found")
        if fading_effect_available:
            fading_compo = fading_component_class('', None, context)
            fading_compo.set_fading(500, 500)
            event.components.append(fading_compo)
        text_tim_entry = TimEntry(((begin, end), ''))
        text_compo = EventComponentText(text, text_tim_entry, context)
        event.components.append(text_compo)
        event.Style = "Credit"
        event.complete(context)
        context["events"]["processed"].append(event)


INSTRUCTIONS = {
    "credit": CreditInstruction,
    "credits": CreditInstruction,
}
