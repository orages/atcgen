"""
atcgen Generator
"""

import os
import logging
import importlib
from pkgutil import iter_modules

from atcgen.event import Event, EventComponentKaraokeSyllable
from atcgen.style import Style
from atcgen.parsers import (INSTRUCTION_PARSER, LYRICS_PARSER,
                            TIM_PARSER, SOFT_BREAK)
from atcgen.utils import ExceptionShield


_LOGGER = logging.getLogger(__name__)

_UNSET = object()


class LyrParser(object):

    def __init__(self, lyr_str):
        self.lyr_str = lyr_str

    def __iter__(self):
        for line in self.lyr_str.split('\n'):
            yield line


class TimParser(object):

    def __init__(self, tim_str):
        self.tim_str = tim_str

    def __iter__(self):
        for line in self.tim_str.split('\n'):
            yield line


class TimEntry(object):

    def __init__(self, parsed_tim):
        super(TimEntry, self).__init__()
        self.times = list(parsed_tim[0])
        self.other = str(parsed_tim[1])

    def __repr__(self):
        return "<{class_name}: (({times}) {other})>".format(
            class_name=self.__class__.__name__,
            times=self.times,
            other=repr(self.other),
        )


def TimEntryGenerator(tim_parser):
    last_time = 0
    for line in tim_parser:
        parsed_tim = TIM_PARSER.parseString(line)
        if parsed_tim:
            tim_entry = TimEntry(parsed_tim)
            if tim_entry.times:
                last_time = tim_entry.times[-1]
        yield tim_entry
    _LOGGER.warning("overiteration, use default")
    while "yield default to avoid raising StopIteration":
        b = last_time
        last_time += 10
        yield TimEntry(((b, last_time), ''))


class Generator(object):

    def __init__(self, instruction_directory=None, renderers_directory=None):
        super(Generator, self).__init__()
        self.instruction_directory = instruction_directory
        self.renderers_directory = renderers_directory
        main_dir = os.path.dirname(__file__)
        if self.instruction_directory is None:
            self.instruction_directory = os.path.join(
                main_dir,
                "instructions",
            )
        if self.renderers_directory is None:
            self.renderers_directory = os.path.join(
                main_dir,
                "renderers",
            )
        self.context = {}
        self.instruction_parser = INSTRUCTION_PARSER
        self.lyrics_parser = LYRICS_PARSER
        self.lyr_parser_class = LyrParser
        self.tim_parser_class = TimParser
        self.instructions = {}
        self.renderers = {}
        self.load_instructions(self.instruction_directory)
        self.load_renderers(self.renderers_directory)

    def generate(self, lyr_str, tim_str, render_format,
                 instruction_directory=None, renderers_directory=None,
                 continue_on_error=False):
        if instruction_directory is None:
            instruction_directory = self.instruction_directory
        self.load_instructions(instruction_directory)
        if renderers_directory is None:
            renderers_directory = self.renderers_directory
        self.load_renderers(renderers_directory)
        self._compile(lyr_str, tim_str, continue_on_error=continue_on_error)
        renderer = self.renderers[render_format]()
        output = renderer.render(self.context)
        return output

    def init_context(self):
        self.context = {
            "_generator": self,
            "ini_data": {},
            "lyr": {
                "path": "",
                "content": "",
            },
            "tim": {
                "path": "",
                "content": "",
            },
            "tass": {
                "path": "",
                "content": "",
            },
            "info": {
                "default": {},
                "attributes": {},
            },
            "styles": {
                "active": None,
                "available": {},
                "used": set(),
            },
            "effects": {
                "karaoke_type": "kt",
            },
            "events": {
                "current": None,
                "event_class": Event,
                "component_syllable_class": (
                    EventComponentKaraokeSyllable
                ),
                "processed": [],
            },
            "hooks": {
                "context.post_init": [],
                "event.pre_create": [],
                "event.post_create": [],
                "event.pre_complete": [],
                "event.post_complete": [],
                "syllable_component.pre_create": [],
                "syllable_component.post_create": [],
                "component.pre_create": [],
                "component.post_create": [],
                "component.pre_append": [],
                "component.post_append": [],
            }
        }
        already_processed = set()
        for instruction_name, instruction_class in self.instructions.items():
            instruction_class_id = id(instruction_class)
            if instruction_class_id in already_processed:
                continue
            instruction_class.set_up(self.context)
            already_processed.add(instruction_class_id)
        default_style = Style()
        styles_available = self.context["styles"]["available"]
        if not self.context["styles"]["active"]:
            if default_style.Name not in styles_available:
                styles_available[default_style.Name] = default_style
            self.context["styles"]["active"] = default_style.Name
        for hook in self.context["hooks"]["context.post_init"]:
            with ExceptionShield():
                hook(self.context)

    def load_instructions(self, directory, update=False):
        if not update:
            self.instructions = {}
        for finder, name, ispkg in iter_modules([directory]):
            _LOGGER.debug("%s", dict(finder=finder, name=name, ispkg=ispkg))
            module_name = '.'.join(("atcgen", "instructions", name))
            spec = finder.find_spec(
                module_name,
                os.path.join(directory, name))
            module = importlib.util.module_from_spec(spec)
            spec.loader.exec_module(module)
            try:
                for name, class_ in module.INSTRUCTIONS.items():
                    if name in self.instructions:
                        _LOGGER.warning(
                            "Instruction named '%s' already exists.".format(
                                name))
                    else:
                        self.instructions[name] = class_
                        _LOGGER.info("instruction '%s' found", name)
            except Exception as e:
                _LOGGER.warning("Fail to load instructions '%s': %s", name, e)

    def load_renderers(self, directory, update=False):
        if not update:
            self.renderers = {}
        for finder, name, ispkg in iter_modules([directory]):
            _LOGGER.debug("%s", dict(finder=finder, name=name, ispkg=ispkg))
            module_name = '.'.join(("atcgen", "renderers", name))
            spec = finder.find_spec(
                module_name,
                os.path.join(directory, name))
            module = importlib.util.module_from_spec(spec)
            spec.loader.exec_module(module)
            try:
                for name, class_ in module.RENDERERS.items():
                    if name in self.renderers:
                        _LOGGER.warning(
                            "renderer for '%s' already exists.".format(
                                name))
                    else:
                        self.renderers[name] = class_
                        _LOGGER.info("renderer for '%s' found", name)
            except Exception as e:
                _LOGGER.warning("Fail to load renderer '%s': %s", name, e)

    def parse_instruction(self, line_str):
        try:
            return self.instruction_parser.parseString(line_str) or None
        except Exception:
            pass
        return None

    def parsed_lyrics(self, line_str):
        try:
            return self.lyrics_parser.parseString(line_str) or None
        except Exception:
            pass
        return None

    def create_event(self):
        for hook in self.context["hooks"]["event.pre_create"]:
            with ExceptionShield():
                hook(self.context)
        event = self.context["events"]["event_class"]()
        for hook in self.context["hooks"]["event.post_create"]:
            with ExceptionShield():
                hook(self.context, event)
        return event

    def complete_event(self, event=None):
        if event is None:
            event = self.current_event
        for hook in self.context["hooks"]["event.pre_complete"]:
            with ExceptionShield():
                hook(self.context, event)
        event.complete(self.context)
        for hook in self.context["hooks"]["event.post_complete"]:
            with ExceptionShield(to_silence=()):
                hook(self.context, event)
        return event

    def create_component(self, syllable_text, tim_entry,
                         component_class=None):
        if component_class is None:
            component_class = self.context["events"][
                "component_syllable_class"]
        for hook in self.context["hooks"]["component.pre_create"]:
            with ExceptionShield():
                hook(self.context)
        component = component_class(syllable_text, tim_entry)
        for hook in self.context["hooks"]["component.post_create"]:
            with ExceptionShield():
                hook(self.context, component)
        return component

    def append_component(self, component, event=None):
        if event is None:
            event = self.current_event
        for hook in self.context["hooks"]["component.pre_append"]:
            with ExceptionShield():
                hook(self.context, event, component)
        event.components.append(component)
        for hook in self.context["hooks"]["component.post_append"]:
            with ExceptionShield(to_silence=()):
                hook(self.context, event, component)
        return event, component

    @property
    def current_event(self):
        return self.context["events"]["current"]

    @current_event.setter
    def current_event(self, value):
        self.context["events"]["current"] = value

    def _compile(self, lyr_str, tim_str, continue_on_error=False):
        self.init_context()
        self.context["lyr"]["content"] = lyr_str
        self.context["tim"]["content"] = tim_str
        lyr_parser = self.lyr_parser_class(lyr_str)
        tim_parser = self.tim_parser_class(tim_str)
        tim_generator = TimEntryGenerator(tim_parser)
        soft_break = False
        context = self.context
        self.current_event = self.create_event()
        for i, line in enumerate(lyr_parser, start=1):
            _LOGGER.debug("process line (%s): %s", i, repr(line))
            try:
                parsed_instruction = self.parse_instruction(line)
                if parsed_instruction:
                    instruction_args_str = parsed_instruction[1]
                    instruction_name = parsed_instruction[0].lower()
                    instruction = self.instructions[instruction_name]()
                    instruction.process(line, instruction_args_str,
                                        context)
                    continue
                parsed_lyrics = self.parsed_lyrics(line)
                if parsed_lyrics:
                    if soft_break is False:
                        self.current_event = self.create_event()
                    if parsed_lyrics[-1] == SOFT_BREAK:
                        soft_break = True
                        parsed_lyrics.pop(-1)
                    else:
                        soft_break = False
                    context["styles"]["used"].add(context["styles"]["active"])
                    context["styles"]["used"].add(context["styles"]["active"])
                    _LOGGER.debug("parsed_lyrics: %s", parsed_lyrics)
                    for syllable_text, tim_entry in zip(parsed_lyrics,
                                                        tim_generator):
                        _LOGGER.debug("syllable: %s (%s)",
                                      syllable_text, tim_entry)
                        component = self.create_component(
                            syllable_text,
                            tim_entry)
                        self.append_component(component)

                    if not soft_break:
                        self.complete_event()
                        context["events"]["processed"].append(
                            self.current_event)
            except Exception as e:
                if not continue_on_error:
                    raise
                _LOGGER.error("Generation failed on line %s: '%s'"
                              " (%s: %s) skip...",
                              i, line, type(e).__name__, e)
        else:
            if soft_break:
                self.complete_event()
                context["events"]["processed"].append(
                    self.current_event)
        self.current_event = None

    def get_instructions_help(self):
        available_instructions = {}
        self.init_context()
        for instruction_name, instruction_class in self.instructions.items():
            instruction_id = id(instruction_class)
            if instruction_id not in available_instructions:
                available_instructions[instruction_id] = {
                    "class": instruction_class,
                    "aliases": [instruction_name],
                }
            else:
                available_instructions[instruction_id]["aliases"].append(
                    instruction_name)

        help_lines = []
        for instruction_id, instruction_data in available_instructions.items():
            headline = ', '.join(instruction_data["aliases"])
            help_lines.append(headline)
            help_lines.append('=' * len(headline))
            desc = instruction_data["class"].help(self.context) or '/'
            help_lines.append(desc)
        return '\n'.join(help_lines)


def main():
    import argparse
    generator_root = os.path.dirname(__file__)
    instruction_directory = os.path.join(generator_root, "instructions")
    parser = argparse.ArgumentParser()
    parser.add_argument("--lyr", default="lyrics.lyr")
    parser.add_argument("--tim", default="timings.tim")
    parser.add_argument("--tass", default="output.tass")
    parser.add_argument("--help-instructions", action="store_true")
    parser.add_argument("--log-level", default="ERROR")
    args = parser.parse_args()
    lyr = args.lyr
    tim = args.tim
    tass = args.tass

    _generator = Generator(instruction_directory=instruction_directory)

    logging.basicConfig(level=args.log_level)

    if args.help_instructions:
        print(_generator.get_instructions_help())
        return

    lyr_str = ""
    with open(lyr, mode='r', encoding="utf-8") as f_lyr:
        lyr_str = f_lyr.read()

    tim_str = ""
    with open(tim, mode='r', encoding="utf-8") as f_tim:
        tim_str = f_tim.read()

    tass_str = _generator.generate(
        lyr_str=lyr_str, tim_str=tim_str,
        render_format="tass", continue_on_error=False)

    with open(tass, mode='w+', encoding="utf-8") as f_tass:
        f_tass.write(tass_str)
