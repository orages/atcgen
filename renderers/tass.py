from itertools import chain
from new_generator.renderer import BaseRenderer
from new_generator.event import (EventComponentText,
                                 EventComponentKaraokeSyllab,
                                 EventComponentEffect)


def timestamp_to_time(ts):
    h, m = divmod(ts, 100 * 60 * 60)
    m, s = divmod(m, 100 * 60)
    s, c = divmod(s, 100)
    string = "{:>01}:{:>02}:{:>02}.{:>02}".format(h, m, s, c)
    return string


def component_to_string(self, event, context):
    karaoke_tag = context["effects"]["karaoke_tag"]
    return "{{{}({},{})}}{}".format(
        karaoke_tag, self.times[0], self.times[-1], self.text)


def escape(text):
    escapped_text = text.replace('\\', "\\\\")
    # escape by inserting zero length word separator character
    escapped_text = escapped_text.replace("\n", "\\N")
    escapped_text = escapped_text.replace("{", "\\{")
    print("ESCAPE", text, "=>", escapped_text)
    return escapped_text

class TassRenderer(BaseRenderer):

    def __init__(self):
        super(TassRenderer, self).__init__()
        self.file_types = {
            key for key, value in RENDERERS.items() if value == self.__class__}
        self.styles_format = (
            "{Name}, {Fontname}, {Fontsize}, {PrimaryColour}, "
            "{SecondaryColour}, {KaraokeColour}, {OutlineColour}, "
            "{BackColour}, {Bold}, {Italic}, {Underline}, "
            "{StrikeOut}, {ScaleX}, {ScaleY}, {Spacing}, "
            "{Angle}, {BorderStyle}, {Outline}, {Shadow}, "
            "{Alignment}, {MarginL}, {MarginR}, {MarginV}, "
            "{Encoding}")
        self.events_format = (
            "{Layer}, {Start}, {End}, {Style}, {Name}, {MarginL}, "
            "{MarginR}, {MarginV}, {Effect}, {Text}")
        self.remove_braces_trans = str.maketrans('', '', "{}")

    def render_script_info(self, info):
        lines = ["[Script Info]"]

        info_dict = info["default"].copy()
        info_dict.update(info["attributes"])
        for key, value in info_dict.items():
            lines.append("{}: {}".format(key, value))
        return '\n'.join(lines)

    def render_styles(self, styles):
        available = styles["available"]
        used = styles["used"]
        lines = ["[V4+ Styles]"]
        format_header = "Format: " + self.styles_format.translate(
            self.remove_braces_trans)
        lines.append(format_header)
        for style_name in used:
            style = available[style_name]
            lines.append("Style: {}".format(
                self.styles_format.format(**style.to_dict())
            ))
        return '\n'.join(lines)

    def escape(self, text):
        pass

    def render_events(self, events):
        events_to_render = events["processed"]
        lines = ["[Events]"]
        format_header = "Format: " + self.events_format.translate(
            self.remove_braces_trans)
        lines.append(format_header)
        for event in events_to_render:
            event_dict = event.to_dict()
            event_dict["Start"] = timestamp_to_time(
                event_dict["start_timestamp"])
            event_dict["End"] = timestamp_to_time(
                event_dict["end_timestamp"])
            event_dict["Text"] = self._render_event_text(event)
            if event_dict["Effect"] is None:
                event_dict["Effect"] = ''
            else:
                event_effect = event_dict["Effect"]
                event_dict["Effect"] = ';'.join(
                    [str(_) for _ in
                     chain((event_effect.name,), event_effect.args)])

            lines.append("Dialogue: {}".format(
                self.events_format.format(**event_dict)
            ))
        return '\n'.join(lines)

    def _render_event_text(self, event):
        text_parts = []
        components = event.components
        for component in components:
            rendering_helper = None
            for format_type in self.file_types:
                if format_type in component.rendering_helpers:
                    rendering_helper = component.rendering_helpers[
                        format_type]
                    text_parts.append(rendering_helper(event,
                                                       escape_fn=escape))
        return ''.join(text_parts)

    def render_lyr(self, lyr):
        lyr_content = lyr["content"]
        lines = ["[lyr]"]
        lines.append(';' + lyr_content.replace('\n', '\n;'))
        return '\n'.join(lines)

    def render_tim(self, tim):
        tim_content = tim["content"]
        lines = ["[tim]"]
        lines.append(';' + tim_content.replace('\n', '\n;'))
        return '\n'.join(lines)

    def render(self, context):
        segments = []
        info_segment = self.render_script_info(context["info"])
        segments.append(info_segment)
        segments.append('\n')
        styles_segment = self.render_styles(context["styles"])
        segments.append(styles_segment)
        segments.append('\n')
        events_segment = self.render_events(context["events"])
        segments.append(events_segment)
        segments.append('\n')
        lyr_segment = self.render_lyr(context["lyr"])
        segments.append(lyr_segment)
        segments.append('\n')
        tim_segment = self.render_tim(context["tim"])
        segments.append(tim_segment)
        return '\n'.join(segments)


RENDERERS = {
    "tass": TassRenderer,
}
