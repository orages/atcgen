import logging
import os
from new_generator.instruction import BaseInstruction

from pyparsing import (Suppress, QuotedString, CharsNotIn, restOfLine)

from pkgutil import iter_modules
import importlib


_LOGGER = logging.getLogger(__name__)
EFFECTS_DIR = os.path.dirname(__file__)

EFFECT_NAME = (
    QuotedString(quoteChar='\'') | QuotedString(quoteChar='"') | CharsNotIn(
        ' ')).setName("name")
EFFECT_ARGS = restOfLine.setName("args")

EFFECT_PARSER = (EFFECT_NAME + Suppress(' ').leaveWhitespace() + EFFECT_ARGS)


class EffectInstruction(BaseInstruction):

    def __init__(self):
        super(EffectInstruction, self).__init__()
        self.full_line = None
        self.args_str = None
        self.context = None
        self.available_effects = EffectInstruction.gather_effects()

    @staticmethod
    def gather_effects(folder=None):
        if folder is None:
            folder = EFFECTS_DIR
        effects_folder = os.path.dirname(__file__)
        name_prefix = __name__
        effects = {}
        for finder, name, ispkg in iter_modules([effects_folder]):
            _LOGGER.debug("%s", dict(finder=finder, name=name, ispkg=ispkg))
            module_name = '.'.join((name_prefix, name))
            spec = finder.find_spec(
                module_name,
                os.path.join(folder, name))
            module = importlib.util.module_from_spec(spec)
            spec.loader.exec_module(module)
            try:
                for name, class_ in module.EFFECTS.items():
                    if name in effects:
                        _LOGGER.warning(
                            "Effect named '%s' already exists.", name)
                    else:
                        effects[name] = class_
                        _LOGGER.info("instruction '%s' found", name)
            except Exception as e:
                _LOGGER.warning("Fail to load instructions '%s': %s", name, e)
        return effects

    @staticmethod
    def set_up(context):
        available_effects = EffectInstruction.gather_effects()
        already_processed = set()
        for effect in available_effects.values():
            effect_id = id(effect)
            if effect_id in already_processed:
                continue
            already_processed.add(effect_id)
            effect.set_up(context)
        context["effects"]["_available"] = available_effects

    def parse(self, args_str):
        parsed_args = EFFECT_PARSER.parseString(self.args_str, parseAll=True)
        return parsed_args

    def process(self, full_line, args_str, context):
        self.full_line = full_line
        self.args_str = args_str
        effects = context["effects"]["_available"]
        parsed_args = self.parse(args_str)
        effect_name = parsed_args[0]
        effect_args = parsed_args[1]
        effect = effects[effect_name]()
        effect.process(full_line, effect_args, context)


class Effect(ABC):

    @staticmethod
    @abstractmethod
    def set_up(context):
        pass

    @staticmethod
    @abstractmethod
    def process(self, full_line, args_str, context):
        pass

    @staticmethod
    @abstractmethod
    def help(context):
        raise NotImplementedError("\"help\" function not defined.")


INSTRUCTIONS = {
    "effect": EffectInstruction,
}
