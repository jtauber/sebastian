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
    octave = 4
    offset = 0
    
    for token in tokenize(s):
        if token in "abcdefg":
            yield (offset, MIDI_NOTE_VALUES[token] + (12 * octave), duration)
            offset += duration
        else:
            raise Exception("unsupported token %s" % token)
