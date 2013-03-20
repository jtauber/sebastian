#!/usr/bin/env python

from sebastian.lilypond.interp import parse
from sebastian.core.transforms import dynamics
from sebastian.midi import write_midi

# construct sequences using lilypond syntax
melody = parse("e4 e f g g f e d c c d e")
A = parse("e4. d8 d2")
Aprime = parse("d4. c8 c2")

two_bars = melody + A + melody + Aprime

velocities = ['pppppp', 'ppppp', 'pppp', 'ppp', 'pp', 'p', 'mp', 'mf', 'f', 'ff', 'fff', 'ffff']

for d in velocities:
    two_bars_with_dynamics = two_bars | dynamics(d)
    write_midi.write('ode_%s.mid' % (d,), [two_bars_with_dynamics])

crescendo = two_bars | dynamics('ppp', 'ff')
write_midi.write('ode_crescendo.mid', [crescendo])

diminuendo = two_bars | dynamics('mf', 'pppp')
write_midi.write('ode_diminuendo.mid', [diminuendo])
