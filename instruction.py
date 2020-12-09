from abc import ABC, abstractmethod


class InstructionError(Exception):
    pass


class InstructionAlreadyExistsError(InstructionError):
    pass


class BaseInstruction(ABC):

    def __init__(self):
        super(BaseInstruction, self).__init__()

    @abstractmethod
    def process(self, full_line, args_str, context):
        pass

    @staticmethod
    @abstractmethod
    def set_up(context):
        pass
