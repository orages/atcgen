import logging
from collections import namedtuple
from new_generator.instruction import BaseInstruction
from new_generator.generator import TimEntry
from new_generator.event import EventComponentText, EventEffect
from new_generator.style import Style
from distutils.util import strtobool

from ..effect import Effect
from pyparsing import (Combine, Group, Optional, Word,
                       alphanums, nums, tokenMap, ParseResults)


PassingEffectArguments = namedtuple("PassingEffectArguments", [
    "direction", "arrival_distance", "arrival_delay",
    "departure_distance", "departure_delay"])


def INTEGER(name):
    """generate INTEGER parser"""
    return Combine(Optional('-') + Word(nums)).setParseAction(
        tokenMap(int)).setName(name)


PASSING_PARSER = Word(alphanums).setParseAction(
    tokenMap(strtobool)).setName(
    "toggle") + Optional(
        Group(Word(alphanums).setName("direction") + INTEGER(
            "arrival_distance") + INTEGER(
            "arrival_delay") + INTEGER("departure_distance") + INTEGER(
            "departure_delay")), ParseResults())

_LOGGER = logging.getLogger(__name__)


class PassingEventEffect(EventEffect):

    def __init__(self, direction, arrival_distance, arrival_delay,
                 departure_distance, departure_delay):
        super(PassingEventEffect, self).__init__()
        self.name = "Passing"
        self.args = PassingEffectArguments(
            direction,
            arrival_distance, arrival_delay,
            departure_distance, departure_delay)


class PassingEffect(Effect):

    def __init__(self):
        super(PassingEffect, self).__init__()
        self.full_line = None

    @staticmethod
    def help(context):
        return (
            "make the event text scroll horizontally across the screen.\n\n"

            "arguments: STATUS DIRECTION ARRIVAL_DISTANCE ARRIVAL_DELAY "
            "DEPARTURE_DISTANCE DEPARTURE_DELAY\n\n"



            "+--------------------+---------------+------------------------+\n"
            "| argument name      | argument type | description            |\n"
            "+====================+===============+========================+\n"
            "| STATUS             | text          | 'y', 'yes', 't',       |\n"
            "|                    |               | 'true',                |\n"
            "|                    |               | 'on' or '1' to enable  |\n"
            "|                    |               | the effect, 'n', 'no', |\n"
            "|                    |               | 'f', 'false', 'off',   |\n"
            "|                    |               | or '0' to disable it.  |\n"
            "+--------------------+---------------+------------------------+\n"
            "| DIRECTION          | integer       | '0' for right to left, |\n"
            "|                    |               | '1' for left to right. |\n"
            "|                    |               |                        |\n"
            "+--------------------+---------------+------------------------+\n"
            "| ARRIVAL_DISTANCE   | integer       | Y coordinate from the  |\n"
            "|                    |               | arriving edge of the   |\n"
            "|                    |               | event, at              |\n"
            "|                    |               | ARRIVAL_DELAY          |\n"
            "|                    |               | milliseconds after the |\n"
            "|                    |               | event begins.          |\n"
            "+--------------------+---------------+------------------------+\n"
            "| ARRIVAL_DELAY      | integer       | time in milliseconds   |\n"
            "|                    | (in ms)       | between the event      |\n"
            "|                    |               | beginning and its      |\n"
            "|                    |               | arrival at             |\n"
            "|                    |               | ARRIVAL_DISTANCE       |\n"
            "+--------------------+---------------+------------------------+\n"
            "| DEPARTURE_DISTANCE | integer       | Y coordinate from the  |\n"
            "|                    |               | departing edge of the  |\n"
            "|                    |               | event, at              |\n"
            "|                    |               | DEPARTURE_DELAY        |\n"
            "|                    |               | milliseconds before    |\n"
            "|                    |               | the event ends.        |\n"
            "+--------------------+---------------+------------------------+\n"
            "| DEPARTURE_DELAY    | integer       | time in milliseconds   |\n"
            "|                    | (in ms)       | between the event      |\n"
            "|                    |               | end and its            |\n"
            "|                    |               | departure from         |\n"
            "|                    |               | DEPARTURE_DISTANCE     |\n"
            "+--------------------+---------------+------------------------+\n"
            '\n'


            "Reference coordinate of the text depends on its Alignment.\n\n"

            "Examples:\n\n"
            "::\n\n"
            "    # text scroll from right of the screen to the left\n"
            "    %effect passing on 0 500 500 500 500\n"
        )

    def parse(self, args_str):
        parsed_args = PASSING_PARSER.parseString(self.args_str, parseAll=True)
        return parsed_args

    def process(self, full_line, args_str, context):
        self.full_line = full_line
        self.args_str = args_str
        is_active, params = self.parse(self.args_str)
        context["effects"]["passing"]["active"] = is_active
        if params:
            context["effects"]["passing"]["params"] = PassingEffectArguments(
                *params)

    @staticmethod
    def set_up(context):
        context["effects"]["passing"] = {
            "active": 0,
            "params": PassingEffectArguments(
                0, 500, 1000, 500, 500
            ),
        }
        context["hooks"]["event.post_complete"].append(
            PassingEffect.event_post_complete_hook
        )

    @staticmethod
    def event_post_complete_hook(context, event):
        passing_context_data = context["effects"]["passing"]
        if event.Effect is not None:
            _LOGGER.error(
                "cannot apply passing to the event "
                "(event %s already has an event effect %s)",
                event, event.Effect)
            return
        elif not passing_context_data.get("active"):
            return
        event.Effect = PassingEventEffect(*passing_context_data["params"])


EFFECTS = {"passing": PassingEffect}
