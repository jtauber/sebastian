#!/usr/bin/env python

## this is the beginning of an experiment for the next level of the algebra

from sebastian.core import DURATION_64
from sebastian.core import VSeq, HSeq, Point, OSequence
from sebastian.core.transforms import midi_pitch, degree_in_key_with_octave, add
from sebastian.core.notes import Key, major_scale

from sebastian.midi import write_midi


def alberti(triad):
    """
    takes a VSeq of 3 notes and returns an HSeq of those notes in an
    alberti figuration.
    """
    return HSeq(triad[i] for i in [0, 2, 1, 2])


# an abstract VSeq of 3 notes in root position (degree 1, 3 and 5)
root_triad = VSeq(Point(degree=n) for n in [1, 3, 5])

quaver_point = Point({DURATION_64: 8})

# an OSequence with alberti figuration repeated 16 times using quavers
alberti_osequence = OSequence(alberti(root_triad) * 16 | add(quaver_point))

C_major = Key("C", major_scale)

# note values filled-out for C major in octave 5 then MIDI pitches calculated
seq = alberti_osequence | degree_in_key_with_octave(C_major, 5) | midi_pitch()

# write to file:
write_midi.write("alberti.mid", [seq])
