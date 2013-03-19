#!/usr/bin/env python

## this is the beginning of an experiment for the next level of the algebra

from sebastian.core import DURATION_64
from sebastian.core import VSeq, HSeq, Point, OSequence
from sebastian.core.transforms import midi_pitch, degree_in_key_with_octave, add
from sebastian.core.notes import Key, major_scale

from sebastian.midi import write_midi

# This is an example of another way to create the song 'shortning bread'

quaver_point = Point({DURATION_64: 8})
quarter_point = Point({DURATION_64: 16})

scale = VSeq(Point(degree=n) for n in [1,2,3,5,6,8])

def make_hseq(notes):
    return HSeq(Point(degree=n, duration_64=d) for n, d in notes)

# produces eighth and quarter notes
hlf = 16
qtr = 8 

# tuples specify pitch and duration
p1 = [(8,qtr),(6,qtr),(5,qtr),(6,qtr)]
p2 = [(8,qtr),(6,qtr),(5,hlf)]
p3 = [(3,qtr),(2,qtr),(1,hlf)]
p4 = [(1,qtr),(6,qtr),(5,qtr),(6,qtr)]
p5 = [(1,qtr),(6,qtr),(5,hlf)]

partA = p1 + p2 + p1 + p3
partB = p4 + p5 + p4 + p3
parts = partA + partA + partB + partB

hseq = make_hseq(parts)

oseq = OSequence(hseq)

C_major = Key("C", major_scale)

# note values filled-out for C major in octave 5 then MIDI pitches calculated
seq = oseq | degree_in_key_with_octave(C_major, 5) | midi_pitch()

write_midi.write("shortning_bread_2.mid", [seq])

