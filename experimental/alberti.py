#!/usr/bin/env python

## this is the beginning of an experiment for the next level of the algebra

import sys
sys.path.append("..")

from core import MIDI_PITCH, OFFSET_64, DURATION_64
from core import OSequence, Point

from midi.player import play

C = OSequence([Point({MIDI_PITCH: 60})])
E = OSequence([Point({MIDI_PITCH: 64})])
G = OSequence([Point({MIDI_PITCH: 67})])

C_major_root = C // E // G

def alberti(triad, duration):
    return OSequence([
        Point({OFFSET_64: 0 * duration, MIDI_PITCH: triad[0][MIDI_PITCH], DURATION_64: duration}),
        Point({OFFSET_64: 1 * duration, MIDI_PITCH: triad[2][MIDI_PITCH], DURATION_64: duration}),
        Point({OFFSET_64: 2 * duration, MIDI_PITCH: triad[1][MIDI_PITCH], DURATION_64: duration}),
        Point({OFFSET_64: 3 * duration, MIDI_PITCH: triad[2][MIDI_PITCH], DURATION_64: duration}),
    ])

play(alberti(C_major_root, 8) * 16)
