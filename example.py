#!/usr/bin/env python

from lilypond.interp import parse
from midi import write_midi, player
from core import OSequence, HSeq, Point, DURATION_64
from core.transforms import transpose, reverse, stretch, invert, add, degree_in_key, midi_pitch
from core.notes import Key, major_scale

# construct sequences using lilypond syntax
seq1 = parse("c d e")
seq2 = parse("e f g")

# concatenate
seq3 = seq1 + seq2

# transpose and reverse
seq4 = seq3 | transpose(12) | reverse()

# merge
seq5 = seq3 // seq4

# play MIDI
player.play(seq5)

# write to MIDI
f = open("seq5.mid", "w")
s = write_midi.SMF(seq5)
s.write(f)
f.close()

# contruct a horizontal sequence of scale degrees
seq6 = HSeq([Point(degree=degree) for degree in [1, 2, 3, 2, 1]])

# put that sequence into C major, octave 4 quavers
C_MAJOR = Key("C", major_scale)
seq7 = seq6 | add({"octave": 4, DURATION_64: 8}) | degree_in_key(C_MAJOR)

# convert to MIDI pitch and play
player.play(OSequence(seq7 | midi_pitch()))
