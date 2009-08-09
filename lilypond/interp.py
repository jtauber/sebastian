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


token_pattern = re.compile("""
    (
        (?P<note>[abcdefg])                     # NOTE
        (?P<octave>'+|,+) ?                     # OCTAVE ?
        ((?P<sharp>(is)*)(?P<flat>(es)*))       # ACCIDENTALS
        |                                       # |
        (?P<rest>r)                             # REST
    )
    (?P<duration>\d+\.*) ?                      # DURATION ?
    """, re.VERBOSE
)


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
    
    for token in tokenize(s):
        m = token_pattern.match(token)
        if m:
            note = m.groupdict()["note"]
            octave_marker = m.groupdict()["octave"]
            duration_marker = m.groupdict()["duration"]
            accidental_sharp = m.groupdict()["sharp"]
            accidental_flat = m.groupdict()["flat"]
            rest = m.groupdict()["rest"]
            accidental_change = 0
            
            if duration_marker is None:
                pass # leave duration the way it was
            else:
                duration = parse_duration(duration_marker)
            if not rest:
                if octave_marker is None:
                    octave = curr_octave
                elif "'" in octave_marker:
                    octave = curr_octave + len(octave_marker)
                elif "," in octave_marker:
                    octave = curr_octave - len(octave_marker)
                if accidental_sharp:
                    accidental_change += len(accidental_sharp) / 2
                if accidental_flat:
                    accidental_change -= len(accidental_flat) / 2
                
                note_value = MIDI_NOTE_VALUES[note] + (12 * octave) + accidental_change
                
                yield (offset, note_value, duration)
            offset += duration
        else:
            raise Exception("unsupported token %s" % token)
