#!/usr/bin/env python

from sebastian.lilypond.interp import parse
from sebastian.midi.write_midi import SMF
from sebastian.core import OSequence, Point, MIDI_PITCH, DURATION_64
from sebastian.core.notes import Key, major_scale
from sebastian.core.transforms import degree_in_key_with_octave, midi_pitch, transpose


# Hanon 1

up_degrees = [1, 3, 4, 5, 6, 5, 4, 3]
down_degrees = [6, 4, 3, 2, 1, 2, 3, 4]
final_degree = [1]

sections = [
    (up_degrees, 4, range(14)),
    (down_degrees, 4, range(13, -2, -1)),
    (final_degree, 32, range(1)),
]

hanon_1 = OSequence()

for section in sections:
    pattern, duration_64, offset = section
    for o in offset:
        for note in pattern:
            hanon_1.append({"degree": note + o, DURATION_64: duration_64})

hanon_1 = hanon_1 | degree_in_key_with_octave(Key("C", major_scale), 4) | midi_pitch()

hanon_rh_1 = hanon_1
hanon_lh_1 = hanon_1 | transpose(-12)

seq = hanon_lh_1 // hanon_rh_1


if __name__ == "__main__":
    f = open("hanon.mid", "w")
    s = SMF([seq])
    s.write(f)
    f.close()
