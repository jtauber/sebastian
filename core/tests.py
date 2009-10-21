#!/usr/bin/env python

import sys; sys.path.append("..")

from core import Point, Sequence
from core import OFFSET_64, MIDI_PITCH, DURATION_64


## points

p1 = Point({
    OFFSET_64: 16,
    MIDI_PITCH: 50,
    DURATION_64: 16,
})

assert p1.tuple(OFFSET_64, DURATION_64) == (16, 16)


## sequences

p2 = Point({
    OFFSET_64: 32,
    MIDI_PITCH: 52,
    DURATION_64: 16,
})

s1 = Sequence([p1, p2])

assert s1 == [
    {DURATION_64: 16, OFFSET_64: 16, MIDI_PITCH: 50},
    {DURATION_64: 16, OFFSET_64: 32, MIDI_PITCH: 52}
]


## concatenation

assert s1 + s1 == [
    {DURATION_64: 16, OFFSET_64: 16, MIDI_PITCH: 50},
    {DURATION_64: 16, OFFSET_64: 32, MIDI_PITCH: 52},
    {DURATION_64: 16, OFFSET_64: 64, MIDI_PITCH: 50},
    {DURATION_64: 16, OFFSET_64: 80, MIDI_PITCH: 52}
]


## repetition

assert s1 * 2 == [
    {DURATION_64: 16, OFFSET_64: 16, MIDI_PITCH: 50},
    {DURATION_64: 16, OFFSET_64: 32, MIDI_PITCH: 52},
    {DURATION_64: 16, OFFSET_64: 64, MIDI_PITCH: 50},
    {DURATION_64: 16, OFFSET_64: 80, MIDI_PITCH: 52}
]

assert s1 * 3 == [
    {DURATION_64: 16, OFFSET_64: 16, MIDI_PITCH: 50},
    {DURATION_64: 16, OFFSET_64: 32, MIDI_PITCH: 52},
    {DURATION_64: 16, OFFSET_64: 64, MIDI_PITCH: 50},
    {DURATION_64: 16, OFFSET_64: 80, MIDI_PITCH: 52},
    {DURATION_64: 16, OFFSET_64: 112, MIDI_PITCH: 50},
    {DURATION_64: 16, OFFSET_64: 128, MIDI_PITCH: 52}
]


## sequence merge

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
    {MIDI_PITCH: 64, OFFSET_64: 0, DURATION_64: 16},
    {MIDI_PITCH: 66, OFFSET_64: 0, DURATION_64: 8},
    {MIDI_PITCH: 66, OFFSET_64: 8, DURATION_64: 8},
    {MIDI_PITCH: 64, OFFSET_64: 16, DURATION_64: 16},
    {MIDI_PITCH: 66, OFFSET_64: 16, DURATION_64: 8},
    {MIDI_PITCH: 66, OFFSET_64: 24, DURATION_64: 8},
    {MIDI_PITCH: 64, OFFSET_64: 32, DURATION_64: 16},
    {MIDI_PITCH: 66, OFFSET_64: 32, DURATION_64: 8},
    {MIDI_PITCH: 66, OFFSET_64: 40, DURATION_64: 8},
    {MIDI_PITCH: 64, OFFSET_64: 48, DURATION_64: 16},
    {MIDI_PITCH: 66, OFFSET_64: 48, DURATION_64: 8},
    {MIDI_PITCH: 66, OFFSET_64: 56, DURATION_64: 8}
]


## point transformation

from core.transforms import transpose

assert s1 | transpose(12) == [
    {MIDI_PITCH: 62, OFFSET_64: 16, DURATION_64: 16},
    {MIDI_PITCH: 64, OFFSET_64: 32, DURATION_64: 16}
]

assert s1 | transpose(5) | transpose(-5) == s1
