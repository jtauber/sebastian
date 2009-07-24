import re

MIDI_NOTE_VALUES = {
    "c": 0,
    "d": 2,
    "e": 4,
    "f": 5,
    "g": 7,
    "a": 9,
    "b": 11,
}


def tokenize(s):
    return s.split()

def parse(s):
    duration = 16
    curr_octave = 4
    offset = 0
    
    for token in tokenize(s):
        m = re.match("(?P<note>[abcdefg])(?P<octave>'+|,+)?(?P<duration>\d+)?", token)
        if m:
            note = m.groupdict()["note"]
            octave_marker = m.groupdict()["octave"]
            duration_marker = m.groupdict()["duration"]
            if octave_marker == "'":
                octave = curr_octave + 1
            elif octave_marker == "''":
                octave = curr_octave + 2
            elif octave_marker == ",":
                octave = curr_octave - 1
            elif octave_marker == ",,":
                octave = curr_octave - 2
            else:
                octave = curr_octave
            note_value = MIDI_NOTE_VALUES[note] + (12 * octave)
            if duration_marker is None:
                pass # leave duration the way it was
            elif duration_marker == "1":
                duration = 64
            elif duration_marker == "2":
                duration = 32
            elif duration_marker == "4":
                duration = 16
            elif duration_marker == "8":
                duration = 8
            else:
                raise Exception("unsupported duration %s" % duration_marker)
            yield (offset, note_value, duration)
            offset += duration
        else:
            raise Exception("unsupported token %s" % token)
