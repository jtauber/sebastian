#!/usr/bin/env python

import sys; sys.path.append("..")

from lilypond.interp import parse
from midi.write_midi import SMF
from core import HSequence, Point, MIDI_PITCH, DURATION_64
from core.notes import major_scale, value, modifiers
from core.transforms import add, degree_in_key


# @@@ won't stay here
class Key:
    def __init__(self, tonic, scale):
        self.notes = scale(value(tonic))
        
    def degree_to_pitch(self, degree):
        return self.notes[degree - 1]


# @@@ won't stay here
def midi_pitch():
    def _(point):
        octave = point["octave"]
        pitch = point["pitch"]
        midi_pitch = [2, 9, 4, 11, 5, 0, 7][pitch % 7]
        midi_pitch += modifiers(pitch)
        midi_pitch += 12 * octave
        point[MIDI_PITCH] = midi_pitch
        return point
    return lambda seq: seq.map_points(_)


degrees = [1, 3, 4, 5, 6, 5, 4, 3]
seq1 = HSequence([Point({"degree": degree}) for degree in degrees])


seq1 = seq1 | degree_in_key(Key("C", major_scale)) | add({"octave": 4}) | \
    add({DURATION_64: 4}) | midi_pitch()

seq = seq1.to_osequence()

if __name__ == "__main__":
    f = open("hanon.mid", "w")
    s = SMF(seq)
    s.write(f)
    f.close()
