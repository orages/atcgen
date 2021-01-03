import logging
import os
import glob
from configparser import RawConfigParser
from new_generator.instruction import BaseInstruction
from new_generator.style import Style
from pyparsing import (Optional, Word, Suppress, QuotedString, Group,
                       ZeroOrMore, alphanums, printables)


_LOGGER = logging.getLogger("generator.instructions.style")
STYLE_DIR = os.path.dirname(__file__)

STYLE_NAME = Word(alphanums).setName("Name") + Optional(
    Suppress(':') + Word(alphanums).setName("Parent")).leaveWhitespace()
STYLE_ASSIGNATION = (
    Word(alphanums) + (
        Suppress('=') + (
            QuotedString(
                '"',
                escChar='\\') | QuotedString(
                '\'',
                escChar='\\') | Word(printables))).leaveWhitespace())
STYLE_PARSER = (Group(STYLE_NAME) + Group(
    ZeroOrMore(Group(STYLE_ASSIGNATION))))


class StyleInstructionError(Exception):
    pass


class StyleAlreadyExistsError(StyleInstructionError):
    pass


class StyleDoesNotExistsError(StyleInstructionError):
    pass


class StyleInstruction(BaseInstruction):

    def __init__(self):
        super(StyleInstruction, self).__init__()
        self.full_line = None
        self.args_str = None
        self.context = None

    def process(self, full_line, args_str, context):
        self.full_line = full_line
        self.args_str = args_str
        self.context = context
        names, attributes = self.parse(self.args_str)
        if len(names) > 1 or attributes:
            self.declare(names, attributes)
        self.set_active(names[0])

    def declare(self, names, attributes, context=None):
        if context is None:
            context = self.context
        styles_available = context["styles"]["available"]
        names, attributes = self.parse(self.args_str)
        attributes = {a[0]: a[1] for a in attributes}
        style = StyleInstruction.create_style(names, attributes,
                                              styles_available)
        style_name = names[0]
        if style_name in styles_available:
            raise StyleAlreadyExistsError(style_name)
        styles_available[style_name] = style

    def set_active(self, name, context=None):
        if context is None:
            context = self.context
        if not context:
            _LOGGER.warning("Cannot set Style '%s' as active "
                            "(invalid context given)", name)
        styles = context["styles"]
        if name not in styles["available"]:
            raise StyleDoesNotExistsError(name)
        styles["active"] = name

    def parse(self, args_str):
        parsed_args = STYLE_PARSER.parseString(args_str, parseAll=True)
        print(parsed_args)
        return parsed_args

    @staticmethod
    def set_up(context):
        context_styles_available = context["styles"]["available"]
        context_styles_used = context["styles"]["used"]
        for path in glob.iglob(os.path.join(STYLE_DIR, "*.ini")):
            styles = StyleInstruction.get_styles_from_ini(path)
            for style_name, style in styles.items():
                if style_name in context_styles_available and\
                   style_name in context_styles_used:
                    _LOGGER.warning("Style '%s' already used "
                                    "redefinition not allowed", style_name)
                context_styles_available[style_name] = style
        context["hooks"]["event.post_create"].append(
            StyleInstruction.event_post_create_hook)

    @staticmethod
    def create_style(names, attributes, styles_dict):
        style_name = names[0]
        style_parent = names[1] if len(names) > 1 else ''
        style_dict = dict(attributes)
        base_dict = {}
        if style_parent:
            if style_parent not in styles_dict:
                raise StyleDoesNotExistsError(style_parent)
            base_dict.update(styles_dict[style_parent].to_dict())
            base_dict.pop("extra_data")
            base_dict.pop("locked")
        base_dict.update(style_dict)
        base_dict.pop("Name", None)
        style = Style(Name=style_name, **base_dict)
        return style

    @staticmethod
    def get_styles_from_ini(ini_path):
        parser = RawConfigParser()
        parser.optionxform = str  # keep leading uppercases
        parser.read(ini_path)
        styles = {}
        for section in sorted(parser.sections(), key=lambda x: (':' in x, x)):
            try:
                splitted_name = section.split(':', 1)
                if len(splitted_name) < 2:
                    splitted_name.append('')
                style_name = splitted_name[0]
                style_dict = dict(parser[section])
                if "Name" in style_dict:
                    _LOGGER.error("Definition of 'Name' in ini section"
                                  " is not allowed, section name will be used"
                                  " '%s'", style_name)
                style = StyleInstruction.create_style(splitted_name,
                                                      style_dict,
                                                      styles)
                if style_name in styles:
                    raise StyleAlreadyExistsError(style_name)
                styles[style_name] = style
            except Exception as e:
                _LOGGER.error("Loading of style %s failed"
                              " (%s: %s) skip...",
                              style_name, type(e).__name__, e)
        return styles

    @staticmethod
    def event_post_create_hook(context, event):
        active_style = context["styles"]["active"]
        event.Style = active_style
        _LOGGER.info("set event style %s", active_style)


INSTRUCTIONS = {
    "style": StyleInstruction,
}
