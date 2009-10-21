from core import MIDI_PITCH, OFFSET_64, DURATION_64

def transpose(semitones):
    def _(point):
        if MIDI_PITCH in point:
            point[MIDI_PITCH] = point[MIDI_PITCH] + semitones
        return point
    return lambda seq: seq.map_points(_)


def shift(offset):
    def _(point):
        point[OFFSET_64] = point[OFFSET_64] + offset
        return point
    return lambda seq: seq.map_points(_)


def stretch(multiplier):
    def _(point):
        point[OFFSET_64] = int(point[OFFSET_64] * multiplier)
        if DURATION_64 in point:
            point[DURATION_64] = int(point[DURATION_64] * multiplier)
        return point
    return lambda seq: seq.map_points(_)
