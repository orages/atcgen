from setuptools import setup, find_packages
import atcgen
version = atcgen.__version__

setup(
    name="atcgen",
    version=version,
    description="Advanced Toyunda Customizable Generator",
    author="Epitanime Toyunda Dev Team",
    author_email="technique@epitanime.com",
    packages=find_packages(),
    package_data={'': ['*']},
    include_package_data=True,
    entry_points={
        "console_scripts": ["atcgen=atcgen.generator:main"]
    }
)
