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

    def parse(self, args_str):
        parsed_args = PASSING_PARSER.parseString(self.args_str, parseAll=True)
        return parsed_args

    def process(self, full_line, args_str, context):
        self.full_line = full_line
        self.args_str = args_str
        is_active, params = parsed_args = self.parse(self.args_str)
        context["effects"]["active"] = is_active
        if params:
            context["effects"]["params"] = PassingEffectArguments(*params)

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
        event.Effect = PassingEventEffect(*passing_context_data["params"])


EFFECTS = {"cursor": PassingEffect}
