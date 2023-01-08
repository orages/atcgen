"""
Entry points & functions to use atcgen without installing it.
"""

from os.path import join as pjoin, dirname, abspath
import importlib
import importlib.machinery
import importlib.util


def get_atcgen_package():
    atcgen_path = pjoin(dirname(dirname(abspath(__file__))), "atcgen")
    finder = importlib.machinery.FileFinder(atcgen_path)
    spec = finder.find_spec(
        "atcgen",
        atcgen_path)
    atcgen = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(atcgen)
    return atcgen


def main():
    pkg = get_atcgen_package()
    from atcgen import generator
    generator.main()


if __name__ == '__main__':
    main()
