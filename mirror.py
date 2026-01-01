#!/usr/bin/env python3
# horizontal character mirroring

a = r"""
                      .-.
                     (   )
                      '-'
                      J L
                      | |
                     J   L
                     |   |
                    J     L
                  .-'.___.'-.
                 /___________\\
            _.- '           'E \._
          .'                       '.
        J                            '.
       F                               L
      J                                 J
     J                                   '
     |                                   L
     |                                   |
     |                                   |
     |                                   J
     |                                    L
     |                                    |
     |             ,.___ ______   ___....--._
     |           ,'     '        '           '-._
     |          J           _____________________'-.
     |         F         .-'   '-88888-'    'Y8888b.'.
     |         |       .'         'P'         '88888b \\
     |         |      J       #     L      #    q8888b L
     |         |      |             |           )8888D )
     |         J      \             J           d8888P P
     |          L      '.         .b.         ,88888P /
     |           '.      '-.___,o88888o.___,o88888P'.'
     |             '-.__________________________..-'
     |                                    |
     |         .-----.........____________J
     |       .' |       |      |       |
     |      J---|-----..|...___|_______|
     |      |   |       |      |       |
     |      Y---|-----..|...___|_______|
     |       '. |       |      |       |
     |         ''-------:....__|______.J
     |                                  |
      L___                              |
          `""----...______________...---' 

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


def mirror_inline(value: str, *, gap: int = 2, seam: str = "") -> str:
    """
    Return: original + gap + (optional seam) + gap + mirrored
    gap: spaces between halves (and around seam if seam provided)
    seam: optional string to put between halves (e.g. " | ")
    """
    value = value.lstrip("\n").rstrip("\n")

    # same swap map used by mirror()
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

    out = []
    spacer = " " * gap
    mid = (spacer + seam + spacer) if seam else spacer

    for line in lines:
        left = line.ljust(w)
        right = left.translate(swap)[::-1]
        out.append(left + mid + right)

    return "\n".join(out)

b = mirror(a)

print(mirror_inline(b, gap=2, seam=" HAPPY NEW YEAR MEATBAGS"))
#mirrored = mirror(a)
#print(mirrored)
#print(a)
#print(mirror_inline(a, gap=4))
