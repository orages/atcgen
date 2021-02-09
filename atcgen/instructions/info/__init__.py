import logging
import os
import glob
from configparser import RawConfigParser
from atcgen.instruction import BaseInstruction, InstructionError
from atcgen.style import Style

from pyparsing import (Suppress, QuotedString, CharsNotIn, restOfLine)


_LOGGER = logging.getLogger(__name__)
INFO_DIR = os.path.dirname(__file__)


ATTRIBUTE_NAME = (
    QuotedString(quoteChar='\'') | QuotedString(quoteChar='"') | CharsNotIn(
        ' ')).setName("name")
ATTRIBUTE_VALUE = restOfLine.setName("value")

INFO_PARSER = (
    ATTRIBUTE_NAME + Suppress(' ').leaveWhitespace() + ATTRIBUTE_VALUE
)


class InfoInstructionError(InstructionError):
    pass


class InfoAlreadyExistsError(InfoInstructionError):
    pass


class InfoInstruction(BaseInstruction):
    ini_file_name = "script_info.ini"
    ini_section_name = "Script Info"

    def __init__(self):
        super(InfoInstruction, self).__init__()
        self.full_line = None
        self.ini_file_name = "script_info.ini"
        self.ini_section_name = "script_info.ini"

    def process(self, full_line, args_str, context):
        self.full_line = full_line
        self.args_str = args_str
        name, value = self.parse(self.args_str)
        _LOGGER.debug("process %s %s", name, value)
        context_info_attributes = context["info"]["attributes"]
        if name in context_info_attributes:
            raise InfoAlreadyExistsError(name)
        context_info_attributes[name] = value

    def parse(self, args_str):
        parsed_args = INFO_PARSER.parseString(args_str, parseAll=True)
        return parsed_args

    @staticmethod
    def set_up(context):
        context_info = context["info"]
        info_ini_path = os.path.join(INFO_DIR, InfoInstruction.ini_file_name)
        info_dict = InfoInstruction.get_info_from_ini(info_ini_path)
        context_info["default"] = info_dict

    @staticmethod
    def help(context):
        return (
            "Declare subtitle file global information.\n\n"

            "arguments: NAME VALUE\n\n"

            "+---------------+---------------+-----------------------------+\n"
            "| argument name | argument type | description                 |\n"
            "+===============+===============+=============================+\n"
            "| NAME          | text          | Name of the info variable   |\n"
            "|               |               | to declare                  |\n"
            "+---------------+---------------+-----------------------------+\n"
            "| VALUE         | text          | Value of the declared       |\n"
            "|               |               | variable                    |\n"
            "+---------------+---------------+-----------------------------+\n"
            '\n'

            "The \"script_info.ini\" file stored in the generator contains"
            "some pre-declared informations.\n"
            "/!\\ script infos act on the whole subtitle file no matter his"
            "position in the lyr.\n\n"

            "Examples:\n\n"
            "::\n\n"
            "    # disable ligatures\n"
            "    %info Ligatures 0\n"
        )

    @staticmethod
    def get_info_from_ini(ini_path):
        parser = RawConfigParser()
        parser.optionxform = str  # keep leading uppercases
        parser.read(ini_path)
        attributes_section = parser[InfoInstruction.ini_section_name]
        return dict(attributes_section)


INSTRUCTIONS = {
    "info": InfoInstruction,
}
