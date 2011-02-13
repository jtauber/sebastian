#!/usr/bin/env python

import sys; sys.path.append("..")

from core import Point, OSequence, HSeq
from core import OFFSET_64, MIDI_PITCH, DURATION_64
from core.notes import Key, major_scale


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

s1 = OSequence([p1, p2])

assert s1._elements == [
    {DURATION_64: 16, OFFSET_64: 16, MIDI_PITCH: 50},
    {DURATION_64: 16, OFFSET_64: 32, MIDI_PITCH: 52}
]

assert s1.last_point() == {
    MIDI_PITCH: 52, OFFSET_64: 32, DURATION_64: 16
}

assert OSequence([]).last_point() == {
    OFFSET_64: 0, DURATION_64: 0
}


## concatenation

assert (s1 + s1)._elements == [
    {DURATION_64: 16, OFFSET_64: 16, MIDI_PITCH: 50},
    {DURATION_64: 16, OFFSET_64: 32, MIDI_PITCH: 52},
    {DURATION_64: 16, OFFSET_64: 64, MIDI_PITCH: 50},
    {DURATION_64: 16, OFFSET_64: 80, MIDI_PITCH: 52}
]

## repetition

assert (s1 * 2)._elements == [
    {DURATION_64: 16, OFFSET_64: 16, MIDI_PITCH: 50},
    {DURATION_64: 16, OFFSET_64: 32, MIDI_PITCH: 52},
    {DURATION_64: 16, OFFSET_64: 64, MIDI_PITCH: 50},
    {DURATION_64: 16, OFFSET_64: 80, MIDI_PITCH: 52}
]

assert (s1 * 3)._elements == [
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

s2 = OSequence([p3]) * 4
s3 = OSequence([p4]) * 8

assert (s2 // s3)._elements == [
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

from core.transforms import transpose, reverse, stretch, invert, add, degree_in_key, midi_pitch

# transpose

assert (s1 | transpose(12))._elements == [
    {MIDI_PITCH: 62, OFFSET_64: 16, DURATION_64: 16},
    {MIDI_PITCH: 64, OFFSET_64: 32, DURATION_64: 16}
]

assert s1 | transpose(5) | transpose(-5) == s1

# reverse

assert (s1 | reverse())._elements == [
    {MIDI_PITCH: 52, OFFSET_64: 0, DURATION_64: 16},
    {MIDI_PITCH: 50, OFFSET_64: 16, DURATION_64: 16},
    {OFFSET_64: 48}
]

assert s1 | reverse() | reverse() == s1

# stretch

assert (s1 | stretch(2))._elements == [
    {MIDI_PITCH: 50, OFFSET_64: 32, DURATION_64: 32},
    {MIDI_PITCH: 52, OFFSET_64: 64, DURATION_64: 32}
]

assert s1 | stretch(2) | stretch(0.5) == s1

# invert

assert (s1 | invert(50))._elements == [
    {DURATION_64: 16, OFFSET_64: 16, MIDI_PITCH: 50},
    {DURATION_64: 16, OFFSET_64: 32, MIDI_PITCH: 48}
]

assert s1 | invert(100) | invert(100) == s1


s4 = HSeq([Point(degree=degree) for degree in [1, 2, 3, 2, 1]])

# add

s5 = s4 | add({"octave": 4, DURATION_64: 8})

assert list(s5) == [
    {'degree': 1, DURATION_64: 8, 'octave': 4},
    {'degree': 2, DURATION_64: 8, 'octave': 4},
    {'degree': 3, DURATION_64: 8, 'octave': 4},
    {'degree': 2, DURATION_64: 8, 'octave': 4},
    {'degree': 1, DURATION_64: 8, 'octave': 4}
]

# degree_in_key

s6 = s5 | degree_in_key(Key("C", major_scale))

assert list(s6) == [
    {'degree': 1, DURATION_64: 8, 'octave': 4, 'pitch': -2},
    {'degree': 2, DURATION_64: 8, 'octave': 4, 'pitch': 0},
    {'degree': 3, DURATION_64: 8, 'octave': 4, 'pitch': 2},
    {'degree': 2, DURATION_64: 8, 'octave': 4, 'pitch': 0},
    {'degree': 1, DURATION_64: 8, 'octave': 4, 'pitch': -2}
]

# midi_pitch

s7 = s6 | midi_pitch()

assert list(s7) == [
    {'degree': 1, MIDI_PITCH: 48, DURATION_64: 8, 'octave': 4, 'pitch': -2},
    {'degree': 2, MIDI_PITCH: 50, DURATION_64: 8, 'octave': 4, 'pitch': 0},
    {'degree': 3, MIDI_PITCH: 52, DURATION_64: 8, 'octave': 4, 'pitch': 2},
    {'degree': 2, MIDI_PITCH: 50, DURATION_64: 8, 'octave': 4, 'pitch': 0},
    {'degree': 1, MIDI_PITCH: 48, DURATION_64: 8, 'octave': 4, 'pitch': -2}
]
