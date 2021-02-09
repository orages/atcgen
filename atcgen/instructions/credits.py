import logging
from atcgen.instruction import BaseInstruction
from atcgen.generator import TimEntry
from atcgen.event import EventComponentText
from atcgen.style import Style

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

    @staticmethod
    def help(context):
        return (
            "Simple credit event generation.\n\n"

            "arguments: START END TEXT\n\n"

            "+-----------------+-----------------+-------------------------+\n"
            "| argument name   | argument type   | description             |\n"
            "+=================+=================+=========================+\n"
            "| START           | timestamp in cs | begining of the event   |\n"
            "+-----------------+-----------------+-------------------------+\n"
            "| END             | timestamp in cs | end of the event        |\n"
            "+-----------------+-----------------+-------------------------+\n"
            "| TEXT            | text            | text to display         |\n"
            "+-----------------+-----------------+-------------------------+\n"
            '\n'

            "Create an event with the \"Credit\" style timed between START AND"
            "END.\n"
            "A default \"Credit\" style is created if none exists"
            " when the line is processed).\n"
            "If the \"fading\" effect is available, a ``fading 500 500`` "
            "is included.\n\n"

            "Examples:\n\n"
            "::\n\n"
            "    # add a credit line at the begining of the video\n"
            "    %credit 0 400 [Serie - Type]\n"
        )

    @staticmethod
    def set_up(context):
        if "Credit" not in context["styles"]["available"]:
            context["styles"]["available"]["Credit"] = Style(
                Name="Credit",
                Fontname="DejaVu Sans",
                Fontsize=25,
                PrimaryColour="&H006044EEEE",
                SecondaryColour="&H006044EEEE",
                KaraokeColour="&H006044EEEE",
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
            from atcgen.instructions.effect.fading import (
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
        context["styles"]["used"].add("Credit")


INSTRUCTIONS = {
    "credit": CreditInstruction,
    "credits": CreditInstruction,
}
