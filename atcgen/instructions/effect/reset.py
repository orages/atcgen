from atcgen.instructions.effect import Effect
from atcgen.event import EventComponentEffect


class EventComponentEffectReset(EventComponentEffect):

    def __init__(self, text='', tim_entry=None, context=None):
        super(EventComponentEffectReset, self).__init__(
            text=text, tim_entry=tim_entry, context=context)
        self.rendering_helpers["tass"] = self._render_tass

    def _render_tass(self, event, escape_fn=None):
        return ("{\\r}")


class ResetEffect(Effect):

    def __init__(self):
        super(ResetEffect, self).__init__()
        self.full_line = None

    def parse(self, args_str):
        return ()

    def set_up(context):
        pass

    @staticmethod
    def help(context):
        return (
            "Reset style override for the remaining of the current event.\n\n"

            "arguments: \n\n"

            "+-----------------+-----------------+-------------------------+\n"
            "| argument name   | argument type   | description             |\n"
            "+=================+=================+=========================+\n"
            "|                 |                 |                         |\n"
            "+-----------------+-----------------+-------------------------+\n"
            '\n'
            "Cancel all style overrides (colours, underline, ...)\n"
            "for the end of the event.\n\n"

            "Examples:\n\n"
            "::\n\n"
            "    # reset all style overrides\n"
            "    %effect reset\n"
        )

    def process(self, full_line, args_str, context):
        self.full_line = full_line
        self.args_str = args_str
        event = context["events"]["current"]
        if event is not None:
            event.components.append(EventComponentEffectReset())


EFFECTS = {"reset": ResetEffect}
