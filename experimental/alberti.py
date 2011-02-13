#!/usr/bin/env python

## this is the beginning of an experiment for the next level of the algebra

import sys
sys.path.append("..")

from core import MIDI_PITCH, OFFSET_64, DURATION_64
from core import VSeq, HSeq, Point, OSequence

from midi.player import play

C = VSeq([Point({MIDI_PITCH: 60})])
E = VSeq([Point({MIDI_PITCH: 64})])
G = VSeq([Point({MIDI_PITCH: 67})])

C_major_root = C // E // G

def alberti(triad, duration):
    """
    takes a VSequence of 3 notes and returns an HSequence of those notes
    in an alberti figuration
    """
    
    return HSeq([
        Point({MIDI_PITCH: triad[0][MIDI_PITCH], DURATION_64: duration}),
        Point({MIDI_PITCH: triad[2][MIDI_PITCH], DURATION_64: duration}),
        Point({MIDI_PITCH: triad[1][MIDI_PITCH], DURATION_64: duration}),
        Point({MIDI_PITCH: triad[2][MIDI_PITCH], DURATION_64: duration}),
    ])

seq = OSequence(alberti(C_major_root, 8) * 16)

play(seq)
