from core import MIDI_PITCH, OFFSET_64, DURATION_64
from core import Point, OSequence


def add(properties):
    def _(point):
        point.update(properties)
        return point
    return lambda seq: seq.map_points(_)


def degree_in_key(key):
    def _(point):
        degree = point["degree"]
        pitch = key.degree_to_pitch(degree)
        point["pitch"] = pitch
        return point
    return lambda seq: seq.map_points(_)


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


def invert(midi_pitch_pivot):
    def _(point):
        if MIDI_PITCH in point:
            interval = point[MIDI_PITCH] - midi_pitch_pivot
            point[MIDI_PITCH] = midi_pitch_pivot - interval
        return point
    return lambda seq: seq.map_points(_)


def reverse():
    def _(sequence):
        new_elements = []
        last_offset = sequence.next_offset()
        if sequence and sequence[0][OFFSET_64] != 0:
            old_sequence = OSequence([Point({OFFSET_64: 0})]) + sequence
        else:
            old_sequence = sequence
        for point in old_sequence:
            new_point = Point(point)
            new_point[OFFSET_64] = last_offset - new_point[OFFSET_64] - new_point.get(DURATION_64, 0)
            if new_point != {OFFSET_64: 0}:
                new_elements.append(new_point)
        return OSequence(sorted(new_elements, key=lambda x: x[OFFSET_64]))
    return _
