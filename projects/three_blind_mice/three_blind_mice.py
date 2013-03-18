#!/usr/bin/env python

from sebastian.lilypond.interp import parse
from sebastian.midi import write_midi

# construct sequences using lilypond syntax
seq1 = parse("e4. d c r")
seq2 = parse("g4. f4 f8 e4.")
seq2a = parse("r4.")
seq2b = parse("r4 g8")
seq3 = parse("c'4 c'8 b a b c'4 g8 g4")
seq3a = parse("g8")
seq3b = parse("f8")

# concatenate
mice = (seq1 * 2) + (seq2 + seq2a) + (seq2 + seq2b) + ((seq3 + seq3a) * 2) + (seq3 + seq3b) + seq1

# write to MIDI
write_midi.write("mice.mid", [mice])
