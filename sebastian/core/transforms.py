from sebastian.core import MIDI_PITCH, OFFSET_64, DURATION_64
from sebastian.core import Point, OSequence

from sebastian.core.notes import modifiers, letter


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


def degree_in_key_with_octave(key, base_octave):
    def _(point):
        degree = point["degree"]
        pitch, octave = key.degree_to_pitch_and_octave(degree)
        point["pitch"] = pitch
        point["octave"] = octave + base_octave
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


def midi_pitch():
    def _(point):
        octave = point["octave"]
        pitch = point["pitch"]
        midi_pitch = [2, 9, 4, 11, 5, 0, 7][pitch % 7]
        midi_pitch += modifiers(pitch)
        midi_pitch += 12 * octave
        point[MIDI_PITCH] = midi_pitch
        return point
    return lambda seq: seq.map_points(_)


def lilypond():
    def _(point):
        if "lilypond" not in point:
            octave = point["octave"]
            pitch = point["pitch"]
            duration = point[DURATION_64]
            if octave > 4:
                octave_string = "'" * (octave - 4)
            elif octave < 4:
                octave_string = "," * (4 - octave)
            else:
                octave_string = ""
            m = modifiers(pitch)
            if m > 0:
                modifier_string = "is" * m
            elif m < 0:
                modifier_string = "es" * m
            else:
                modifier_string = ""
            pitch_string = letter(pitch).lower() + modifier_string
            duration_string = str(int(64 / duration))  # @@@ doesn't handle dotted notes yet
            point["lilypond"] = "%s%s%s" % (pitch_string, octave_string, duration_string)
        return point
    return lambda seq: seq.map_points(_)
