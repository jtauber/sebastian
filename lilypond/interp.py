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

# Cutting up the regex into manageable components - helps with testing
RE_NOTE = "(?P<note>[abcdefg])"
RE_8VE = "(?P<octave>'+|,+)"
RE_REST = "(?P<rest>r)"
RE_DURATION = "(?P<duration>\d+\.*)"
RE_SHARP = "(?P<sharp>(is)*)"
RE_FLAT = "(?P<flat>(es)*)"
RE_ACCIDENTALS = "(%s%s)?"%(RE_SHARP, RE_FLAT)

def tokenize(s):
    return s.split()


def parse_duration(duration_marker):
    if "." in duration_marker:
        first_dot = duration_marker.find(".")
        core = int(duration_marker[:first_dot])
        # this doesn't actually check they are all dots, but regex wouldn't
        # match in the first place otherwise
        dots = len(duration_marker[first_dot:])
    else:
        core = int(duration_marker)
        dots = 0
    
    duration = (2 - (2**-dots)) * 64 / core
    
    return duration


def parse(s):
    duration = 16
    curr_octave = 4
    offset = 0
    token_matcher = "(%s%s?%s|%s)%s?"%(RE_NOTE, RE_8VE, RE_ACCIDENTALS, RE_REST,
            RE_DURATION)
    
    for token in tokenize(s):
        m = re.match(token_matcher, token)
        if m:
            note = m.groupdict()["note"]
            octave_marker = m.groupdict()["octave"]
            duration_marker = m.groupdict()["duration"]
            accidental_sharp = m.groupdict()["sharp"]
            accidental_flat = m.groupdict()["flat"]
            rest = m.groupdict()["rest"]
            accidental_change = 0
            print m.groupdict()
            if duration_marker is None:
                pass # leave duration the way it was
            else:
                duration = parse_duration(duration_marker)
            if not rest:
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
                if accidental_sharp:
                    accidental_change+=len(accidental_sharp)/2
                if accidental_flat:
                    accidental_change-=len(accidental_flat)/2
                note_value = MIDI_NOTE_VALUES[note] + (12 * octave) +\
                        accidental_change
                yield (offset, note_value, duration)
            offset += duration
        else:
            raise Exception("unsupported token %s" % token)
