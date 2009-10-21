from core import MIDI_PITCH, OFFSET_64


def transpose(semitones):
    def _(point):
        point[MIDI_PITCH] = point[MIDI_PITCH] + semitones
        return point
    return _


def shift(offset):
    
    def _(point):
        point[OFFSET_64] = point[OFFSET_64] + offset
        return point
    return _
