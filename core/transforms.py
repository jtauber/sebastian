from core import MIDI_PITCH, OFFSET_64, DURATION_64
from core import Point, Sequence
from core import shift


def transpose(semitones):
    def _(point):
        if MIDI_PITCH in point:
            point[MIDI_PITCH] = point[MIDI_PITCH] + semitones
        return point
    return lambda seq: seq.map_points(_)


def stretch(multiplier):
    def _(point):
        point[OFFSET_64] = int(point[OFFSET_64] * multiplier)
        if DURATION_64 in point:
            point[DURATION_64] = int(point[DURATION_64] * multiplier)
        return point
    return lambda seq: seq.map_points(_)


def reverse():
    def _(sequence):
        new_sequence = []
        last_offset = sequence.last_point()[OFFSET_64]
        for point in sorted(sequence, key=lambda x: x[OFFSET_64], reverse=True):
            new_point = Point(point)
            new_point[OFFSET_64] = last_offset - new_point[OFFSET_64]
            new_sequence.append(new_point)
        return new_sequence
    return _