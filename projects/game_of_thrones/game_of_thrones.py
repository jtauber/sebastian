"""
The main title theme to HBO's Game of Thrones by Ramin Djawadi
"""

from sebastian.core import Point, HSeq, OSequence
from sebastian.core.transforms import midi_pitch, degree_in_key, add
from sebastian.core.notes import Key, major_scale, minor_scale
from sebastian.midi import write_midi

C_Major = Key("C", major_scale)
C_minor = Key("C", minor_scale)

motive_degrees = HSeq(Point(degree=n) for n in [5, 1, 3, 4])

motive_rhythm_1 = HSeq(Point(duration_64=n) for n in [16, 16, 8, 8])
motive_rhythm_2 = HSeq(Point(duration_64=n) for n in [48, 48, 8, 8, 32, 32, 8, 8])

motive_1 = motive_degrees & motive_rhythm_1
motive_2 = (motive_degrees * 2) & motive_rhythm_2

# add key and octave
seq1 = (motive_1 * 4) | add({"octave": 5}) | degree_in_key(C_minor)
seq2 = (motive_1 * 4) | add({"octave": 5}) | degree_in_key(C_Major)
seq3 = motive_2 | add({"octave": 4}) | degree_in_key(C_minor)

seq = (seq1 + seq2 + seq3) | midi_pitch() | OSequence

write_midi.write("game_of_thrones.mid", [seq], instruments=[49], tempo=350000)
