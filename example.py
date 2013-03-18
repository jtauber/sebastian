#!/usr/bin/env python

from sebastian.lilypond.interp import parse
from sebastian.midi import write_midi, player
from sebastian.core import OSequence, HSeq, Point, DURATION_64
from sebastian.core.transforms import transpose, reverse, add, degree_in_key, midi_pitch
from sebastian.core.notes import Key, major_scale

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
player.play([seq5])

# write to MIDI
write_midi.write("seq5.mid", [seq5])

# contruct a horizontal sequence of scale degrees
seq6 = HSeq(Point(degree=degree) for degree in [1, 2, 3, 2, 1])

# put that sequence into C major, octave 4 quavers
C_MAJOR = Key("C", major_scale)
seq7 = seq6 | add({"octave": 4, DURATION_64: 8}) | degree_in_key(C_MAJOR)

# convert to MIDI pitch and play
player.play([OSequence(seq7 | midi_pitch())])
