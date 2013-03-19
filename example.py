#!/usr/bin/env python

from sebastian.lilypond.interp import parse
from sebastian.lilypond.write_lilypond import write
from sebastian.midi import write_midi, player
from sebastian.core import OSequence, HSeq, Point, DURATION_64
from sebastian.core.transforms import transpose, reverse, add, degree_in_key, midi_pitch, lilypond
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


# sequence of first four degree of a scale
seq8 = HSeq(Point(degree=n) for n in [1, 2, 3, 4])

# add duration and octave
seq8 = seq8 | add({DURATION_64: 16, "octave": 5})

# put into C major
seq8 = seq8 | degree_in_key(C_MAJOR)

# annotate with lilypond
seq8 = seq8 | lilypond()

# write out lilypond file
write("example.ly", seq8)
