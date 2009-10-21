#!/usr/bin/env python

import sys; sys.path.append("..")

from lilypond.interp import parse
from midi.write_midi import SMF
from core import Sequence

rh = parse(r"""
    \relative c'' {
        g16 fis g8 ~ g16 d16 e fis g a b cis
        d16 cis d8 ~ d16 a16 b cis d e fis d
        g16 fis g8 ~ g16 fis16 e d cis e a, g
        fis e d cis d fis a, g fis a d,8
    }""")

lh = parse(r"""
    \relative c {
        g8 b'16 a b8 g g, g'
        fis,8 fis'16 e fis8 d fis, d'
        e,8 e'16 d e8 g a, cis'
        d, fis16 e fis8 d d,
    }""")

# operator overloading FTW!
seq = rh // lh

if __name__ == "__main__":
    f = open("var1.mid", "w")
    s = SMF(seq)
    s.write(f)
    f.close()
