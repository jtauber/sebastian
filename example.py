from lilypond.interp import parse
from midi import write_midi, player
from core.transforms import transpose, reverse, stretch, invert

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
