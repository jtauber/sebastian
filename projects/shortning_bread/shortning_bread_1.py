#!/usr/bin/env python

## this is the beginning of an experiment for the next level of the algebra

from sebastian.core import DURATION_64
from sebastian.core import VSeq, HSeq, Point, OSequence
from sebastian.core.transforms import midi_pitch, degree_in_key_with_octave, add
from sebastian.core.notes import Key, major_scale

from sebastian.midi import write_midi

quaver_point = Point({DURATION_64: 8})
quarter_point = Point({DURATION_64: 16})

# this song uses only these notes
scale = VSeq(Point(degree=n) for n in [1,2,3,5,6,8])

# the following functions all create sequences of eighth notes
def h1(scale):
    return HSeq(scale[i] for i in [5, 4, 3, 4]) | add(quaver_point)

def h1_end1(scale):
    return HSeq(scale[i] for i in [5, 4]) | add(quaver_point) 

def end(scale):
    return HSeq(scale[i] for i in [2, 1]) | add(quaver_point)

def h2(scale):
    return HSeq(scale[i] for i in [0, 4, 3, 4]) | add(quaver_point)

def h2_end1(scale):
    return HSeq(scale[i] for i in [0, 4]) | add(quaver_point)

# there's two important quarter notes used at the ends of sections
e1 = HSeq(scale[3]) | add(quarter_point)
e2 = HSeq(scale[0]) | add(quarter_point)

partA = h1(scale) + h1_end1(scale) + e1 + h1(scale) + end(scale) + e2 
partB = h2(scale) + h2_end1(scale) + e1 + h2(scale) + end(scale) + e2

# here we see the basic structure of the song
oseq = OSequence((partA * 2) + (partB * 2))

C_major = Key("C", major_scale)

# note values filled-out for C major in octave 5 then MIDI pitches calculated
seq = oseq | degree_in_key_with_octave(C_major, 5) | midi_pitch()

# write to file:
write_midi.write("shortning_bread_1.mid", [seq])
