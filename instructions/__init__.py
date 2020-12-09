import importlib
import os
from pkgutil import iter_modules
import logging

_LOGGER = logging.getLogger("instructions")


# def load_instructions(path, name_prefix="instructions"):
#     instructions = {}
#     for finder, name, ispkg in iter_modules([path]):
#         module_name = '.'.join((name_prefix, name))
#         spec = finder.find_spec(
#             module_name,
#             os.path.join(path, name))
#         module = importlib.util.module_from_spec(spec)
#         spec.loader.exec_module(module)
#         try:
#             for name, class_ in module.INSTRUCTIONS.items():
#                 if name in instructions:
#                     raise InstructionAlreadyExistsError(
#                         "Instruction named '{}' already exists.".format(
#                             name))
#                 else:
#                     instructions[name] = class_
#                     _LOGGER.info("instruction '%s' found", name)
#         except Exception as e:
#             _LOGGER.warning("Fail to load instructions '%s': %s", name, e)
#     return instructions
