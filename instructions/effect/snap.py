from new_generator.instructions.effect import Effect

from pyparsing import (Combine, Word, nums, tokenMap)


SNAP_ARG = Combine(Word(nums)).setParseAction(
    tokenMap(int)).setName("value")


class SnapEffect(Effect):

    def __init__(self):
        super(SnapEffect, self).__init__()
        self.full_line = None

    def parse(self, args_str):
        parsed_args = SNAP_ARG.parseString(self.args_str, parseAll=True)
        return parsed_args

    @staticmethod
    def help(context):
        return (
            "Snap successive syllables with close enough timings.\n\n"

            "Active by default.\n"
            "arguments: VALUE\n\n"


            "+---------------+---------------+-----------------------------+\n"
            "| argument name | argument type | description                 |\n"
            "+===============+===============+=============================+\n"
            "| VALUE         | integer       | Maximum timing difference   |\n"
            "|               |               | to snap                     |\n"
            "+---------------+---------------+-----------------------------+\n"
            '\n'

            "Snaping is done by moving the beginning of the syllable at the "
            "centisecond following the end of the previous syllable.\n\n"

            "Examples:\n\n"
            "::\n\n"
            "    # disable snapping\n"
            "    %effect snap 0\n"
        )

    def process(self, full_line, args_str, context):
        self.full_line = full_line
        self.args_str = args_str
        parsed_args = self.parse(self.args_str)
        value = parsed_args[0]
        context["effects"]["snap"] = value

    @staticmethod
    def set_up(context):
        context["effects"]["snap"] = 20
        context["hooks"]["component.pre_append"].append(
            SnapEffect.component_pre_append_hook
        )

    @staticmethod
    def component_pre_append_hook(context, event, component):
        previous_component = None
        if not event.components:
            return

        previous_component = event.components[-1]

        component_begin = component.get_begining_timestamp()
        previous_component_end = previous_component.get_ending_timestamp()

        if component_begin is None or previous_component_end is None:
            return

        delta = component_begin - previous_component_end
        if delta > 0 and delta <= context["effects"].get("snap", 0):
            component.times[0] = previous_component_end + 1


EFFECTS = {"snap": SnapEffect}
