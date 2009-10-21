from core import MIDI_PITCH


def transpose(semitones):
    def _(point):
        point[MIDI_PITCH] = point[MIDI_PITCH] + semitones
        return point
    return _
