#!/usr/bin/env python3
# horizontal character mirroring

a = r"""
                      .-.
                     (   )
                      '-'
                      J L
                      | |
"""

def mirror(value: str) -> str:
    value = value.lstrip("\n").rstrip("\n")
    swap = str.maketrans({
        "/": "\\",
        "\\": "/",
        "(": ")",
        ")": "(",
        "[": "]",
        "]": "[",
        "{": "}",
        "}": "{",
        "<": ">",
        ">": "<",
        "L": "J",
        "J": "L",
    })

    lines = value.splitlines()
    w = max((len(line) for line in lines), default=0)

    # pad so whitespace mirrors too, then swap directional chars, then reverse
    return "\n".join(line.ljust(w).translate(swap)[::-1] for line in lines)

mirrored = mirror(a)
print(mirrored)
'''
should really just finish this RN
but it do work
'''
