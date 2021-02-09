import copy
from atcgen.instructions.effect import Effect
from atcgen.event import EventComponentEffect, EventComponentText

from pyparsing import (Word, alphanums)
from distutils.util import strtobool

CURSOR_ARG = Word(alphanums).setName("value")


class EventComponentEffectCursor(EventComponentEffect):

    def __init__(self, text='', tim_entry=None, context=None):
        super(EventComponentEffectCursor, self).__init__(
            text=text, tim_entry=tim_entry, context=context)
        self.rendering_helpers["tass"] = self._render_tass

    def _render_tass(self, event, escape_fn=None):
        event_start = event.start_timestamp
        start_offset = self.get_begining_timestamp() - event_start
        duration = self.get_ending_timestamp() - self.get_begining_timestamp()
        text = self.text
        if escape_fn is not None:
            text = escape_fn(text)
        return (
            "{{\\pc({start_offset}, {duration})}}{text}".format(
                start_offset=start_offset, duration=duration, text=text))


class EventComponentEffectPlaceholder(EventComponentEffect):

    def __init__(self, text='', tim_entry=None, context=None):
        super(EventComponentEffectPlaceholder, self).__init__(
            text=text, tim_entry=tim_entry, context=context)
        self.rendering_helpers["tass"] = self._render_tass

    def _render_tass(self, event, escape_fn=None):
        event_start = event.start_timestamp
        start_offset = self.get_begining_timestamp() - event_start
        duration = self.get_ending_timestamp() - self.get_begining_timestamp()
        text = self.text
        if escape_fn is not None:
            text = escape_fn(text)
        return (
            "{{\\ph({start_offset}, {duration})}}{text}".format(
                start_offset=start_offset, duration=duration, text=text))


class CursorEffect(Effect):

    def __init__(self):
        super(CursorEffect, self).__init__()
        self.full_line = None

    def parse(self, args_str):
        parsed_args = CURSOR_ARG.parseString(self.args_str, parseAll=True)
        return parsed_args

    @staticmethod
    def help(context):
        return (
            "Add a line of cursors matching the karaoke syllables.\n\n"

            "Active by default.\n\n"
            "arguments: STATUS\n\n"

            "+-----------------+-----------------+-------------------------+\n"
            "| argument name   | argument type   | description             |\n"
            "+=================+=================+=========================+\n"
            "| STATUS          | text            | 'y', 'yes', 't',        |\n"
            "|                 |                 | 'true',                 |\n"
            "|                 |                 | 'on' or '1' to enable   |\n"
            "|                 |                 | the effect, 'n', 'no',  |\n"
            "|                 |                 | 'f', 'false', 'off',    |\n"
            "|                 |                 | or '0' to disable it.   |\n"
            "+-----------------+-----------------+-------------------------+\n"
            '\n'
            "If the cursor is disabled or (re-enabled) in the middle of an "
            "event, place-holder components are inserted to avoid "
            "misalignment of syllables.\n\n"

            "Examples:\n\n"
            "::\n\n"
            "    # disable the cursor\n"
            "    %effect cursor off\n"
        )

    def process(self, full_line, args_str, context):
        self.full_line = full_line
        self.args_str = args_str
        parsed_args = self.parse(self.args_str)
        value = strtobool(parsed_args[0])
        context["effects"]["cursor"] = value

    @staticmethod
    def set_up(context):
        context["effects"]["cursor"] = 1
        context["hooks"]["component.post_append"].append(
            CursorEffect.component_post_append_hook
        )
        context["hooks"]["event.pre_complete"].append(
            CursorEffect.event_pre_complete_hook
        )

    @staticmethod
    def event_pre_complete_hook(context, event):
        extra_data = event.extra_data
        if "cursor_components" not in extra_data:
            return
        for component in extra_data["cursor_components"]:
            if isinstance(component, EventComponentEffectCursor):
                break
        else:
            return
        new_line_component = EventComponentText('\n', None, context)
        # add newline without triggering hooks
        event.components.append(new_line_component)
        # add cursor components
        generator = context["_generator"]
        for cursor_component in extra_data["cursor_components"]:
            generator.append_component(cursor_component, event=event)

    @staticmethod
    def component_post_append_hook(context, event, component):
        if isinstance(component, (EventComponentEffect)):
            return
        extra_data = event.extra_data
        cursor_effect_status = context["effects"].get("cursor", True)
        if cursor_effect_status:
            component_class = EventComponentEffectCursor
        else:
            component_class = EventComponentEffectPlaceholder
        cursor_component = component_class()
        cursor_component.times = copy.deepcopy(component.times)
        cursor_component.text = copy.deepcopy(component.text)
        if "cursor_components" not in extra_data:
            extra_data["cursor_components"] = []
        extra_data["cursor_components"].append(cursor_component)


EFFECTS = {"cursor": CursorEffect}
