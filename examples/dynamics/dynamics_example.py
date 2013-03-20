#!/usr/bin/env python
"""
Generate ode to joy in the entire dynamic range 'pppppp' -> 'ffff'. Also generate a crescendo from 'ppp' to 'ff' and a dimininuendo from 'mf' to 'ppp'.

This will output numerous midi files, as well as three lilypond (*.ly) files with dynamic notation.
"""

from sebastian.lilypond.interp import parse
from sebastian.core.transforms import dynamics, lilypond, midi_to_pitch, add
from sebastian.midi import write_midi
from sebastian.lilypond import write_lilypond

# construct sequences using lilypond syntax
melody = parse("e4 e f g g f e d c c d e")
A = parse("e4. d8 d2")
Aprime = parse("d4. c8 c2")

two_bars = melody + A + melody + Aprime
two_bars = two_bars | midi_to_pitch()
two_bars = two_bars | add({"octave": 5})

velocities = ['pppppp', 'ppppp', 'pppp', 'ppp', 'pp', 'p', 'mp', 'mf', 'f', 'ff', 'fff', 'ffff']

for d in velocities:
    two_bars_with_dynamics = two_bars | dynamics(d)
    write_midi.write('ode_%s.mid' % (d,), [two_bars_with_dynamics])

two_bars_ff_lily = two_bars | dynamics('ff') | lilypond()
write_lilypond.write('ode_ff.ly', two_bars_ff_lily)

crescendo = two_bars | dynamics('ppp', 'ff')
write_midi.write('ode_crescendo.mid', [crescendo])
write_lilypond.write('ode_crescendo.ly', crescendo | lilypond())

diminuendo = two_bars | dynamics('mf', 'pppp')
write_midi.write('ode_diminuendo.mid', [diminuendo])
write_lilypond.write('ode_diminuendo.ly', diminuendo | lilypond())
