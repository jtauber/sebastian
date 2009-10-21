#!/usr/bin/env python

import sys; sys.path.append("..")

from core import Point, Sequence
from core import OFFSET_64, MIDI_PITCH, DURATION_64


p1 = Point({
    OFFSET_64: 16,
    MIDI_PITCH: 50,
    DURATION_64: 16,
})

assert p1.tuple(OFFSET_64, DURATION_64) == (16, 16)

p2 = Point({
    OFFSET_64: 32,
    MIDI_PITCH: 52,
    DURATION_64: 16,
})

s1 = Sequence([p1, p2])

assert s1 == [
    {'duration_64': 16, 'offset_64': 16, 'midi_pitch': 50},
    {'duration_64': 16, 'offset_64': 32, 'midi_pitch': 52}
]

assert s1 + s1 == [
    {'duration_64': 16, 'offset_64': 16, 'midi_pitch': 50},
    {'duration_64': 16, 'offset_64': 32, 'midi_pitch': 52},
    {'duration_64': 16, 'offset_64': 64, 'midi_pitch': 50},
    {'duration_64': 16, 'offset_64': 80, 'midi_pitch': 52}
]

assert s1 * 2 == [
    {'duration_64': 16, 'offset_64': 16, 'midi_pitch': 50},
    {'duration_64': 16, 'offset_64': 32, 'midi_pitch': 52},
    {'duration_64': 16, 'offset_64': 64, 'midi_pitch': 50},
    {'duration_64': 16, 'offset_64': 80, 'midi_pitch': 52}
]

assert s1 * 3 == [
    {'duration_64': 16, 'offset_64': 16, 'midi_pitch': 50},
    {'duration_64': 16, 'offset_64': 32, 'midi_pitch': 52},
    {'duration_64': 16, 'offset_64': 64, 'midi_pitch': 50},
    {'duration_64': 16, 'offset_64': 80, 'midi_pitch': 52},
    {'duration_64': 16, 'offset_64': 112, 'midi_pitch': 50},
    {'duration_64': 16, 'offset_64': 128, 'midi_pitch': 52}
]

p3 = Point({
    OFFSET_64: 0,
    MIDI_PITCH: 64,
    DURATION_64: 16,
})

p4 = Point({
    OFFSET_64: 0,
    MIDI_PITCH: 66,
    DURATION_64: 8,
})

s2 = Sequence([p3]) * 4
s3 = Sequence([p4]) * 8

assert s2 // s3 == [
    {'midi_pitch': 64, 'offset_64': 0, 'duration_64': 16},
    {'midi_pitch': 66, 'offset_64': 0, 'duration_64': 8},
    {'midi_pitch': 66, 'offset_64': 8, 'duration_64': 8},
    {'midi_pitch': 64, 'offset_64': 16, 'duration_64': 16},
    {'midi_pitch': 66, 'offset_64': 16, 'duration_64': 8},
    {'midi_pitch': 66, 'offset_64': 24, 'duration_64': 8},
    {'midi_pitch': 64, 'offset_64': 32, 'duration_64': 16},
    {'midi_pitch': 66, 'offset_64': 32, 'duration_64': 8},
    {'midi_pitch': 66, 'offset_64': 40, 'duration_64': 8},
    {'midi_pitch': 64, 'offset_64': 48, 'duration_64': 16},
    {'midi_pitch': 66, 'offset_64': 48, 'duration_64': 8},
    {'midi_pitch': 66, 'offset_64': 56, 'duration_64': 8}
]
