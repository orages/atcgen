from pyparsing import (CaselessKeyword, CharsNotIn, Combine, Group, Keyword,
                       Literal, OneOrMore, Optional, Regex, Suppress, Word,
                       ZeroOrMore, alphanums, nums, replaceWith, restOfLine)


def LyrInstruction(name, caseless=True):
    constructor = CaselessKeyword if caseless else Keyword
    return (Suppress('%') + constructor(name)).leaveWhitespace()


SOFT_BREAK = type("SOFT_BREAK",
                  (object,),
                  {"__repr__": lambda self: "<SOFT_BREAK>"})()


INSTRUCTION_PARSER = Suppress('%') + Word(alphanums) + restOfLine


CREDIT_TIMES = Word(nums) + Word(nums)
CREDIT_PARSER = LyrInstruction("credit") + Group(CREDIT_TIMES) + restOfLine

EFFECT_PARSER = LyrInstruction("effect") + Word(alphanums) + restOfLine


ESCAPE = Suppress(Literal("\\")) + Word("\\)]:", exact=1)
TEXT = Combine(ZeroOrMore(ESCAPE ^ Regex("[^\\]\\\\:]")))

syllable = CharsNotIn("&\\")

split_word = Suppress('&') + ZeroOrMore(
    syllable + ZeroOrMore(Suppress('\\') + (
                          (Literal('\\') | Literal('&') | Literal(
                              'n').setParseAction(
                              replaceWith('\n')) | syllable)))
).setParseAction(lambda t: ''.join(t))

LYRICS_PARSER = ZeroOrMore(split_word) + Optional(
    Literal('\\')).setParseAction(lambda s: SOFT_BREAK if s else None)

TIM_PARSER = Group(
    OneOrMore(Word(nums).setParseAction(lambda l: [int(s) for s in l]))
) + restOfLine
