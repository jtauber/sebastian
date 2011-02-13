#!/usr/bin/env python

import sys; sys.path.append("..")

from lilypond.interp import parse
from midi.write_midi import SMF
from core import OSequence, HSeq, Point, MIDI_PITCH, DURATION_64
from core.notes import Key, major_scale
from core.transforms import add, degree_in_key, midi_pitch


degrees = [1, 3, 4, 5, 6, 5, 4, 3]
seq1 = HSeq([Point({"degree": degree}) for degree in degrees])


seq1 = seq1 | degree_in_key(Key("C", major_scale)) | add({"octave": 4}) | \
    add({DURATION_64: 4}) | midi_pitch()

seq = OSequence(seq1)


if __name__ == "__main__":
    f = open("hanon.mid", "w")
    s = SMF(seq)
    s.write(f)
    f.close()
