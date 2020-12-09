class BaseRenderer(object):
    def render(self, context):
        raise NotImplementedError


class ScriptInfoRenderer(BaseRenderer):
    def __init__(self):
        self.section_name = "Script Info"
        super(ScriptInfoRenderer, self).__init__()

    def render(self, context):
        raise NotImplementedError


class StylesRenderer(BaseRenderer):
    pass


class EventsRenderer(BaseRenderer):
    pass


class LyrRenderer(BaseRenderer):
    pass


class TimRenderer(BaseRenderer):
    pass
