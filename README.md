Advanced Toyunda Customizable GENerator
=======================================


Description
-----------


###Goal
Easy to use & customize toyunda generator, compile .tim & .lyr files to .tass files.


###features

input lyrics formats:
 - .lyr
input time formats:
 - .tim
output formats:
 - .tass

built-in instructions:
 - %info
 - %Style
 - %color
 - %credits
 - %effect
   - cursor
   - fading
   - move
   - passing
   - position
   - snap


Setup
-----
1. Install requirements
```
pip install -r requirements.txt
```
2. Build docs (pdf)
```
sphinx-build -b pdf doc doc_build
```
OR
2. Build docs (html)
```
sphinx-build doc doc_build
```


Usage
-----
usage: atcgen [-h] [--lyr LYR] [--tim TIM] [--tass TASS] [--help-instructions] [--log-level LOG_LEVEL]

optional arguments:
  -h, --help            show this help message and exit
  --lyr LYR
  --tim TIM
  --tass TASS
  --help-instructions
  --log-level LOG_LEVEL
