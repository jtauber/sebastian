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


token_pattern = re.compile(r"""^\s*                 # INITIAL WHITESPACE
    (
        (                                           # NOTE
            (
                (?P<note>[abcdefg])                     # NOTE NAME
                (?P<octave>'+|,+) ?                     # OCTAVE ?
                ((?P<sharp>(is)+)|(?P<flat>(es)+)) ?    # ACCIDENTALS ?
                |                                       # |
                (?P<rest>r)                             # REST
            )
            (?P<duration>\d+\.*) ?                      # DURATION ?
        )
        |
        (?P<tie>~)                                  # TIE
        |
        \\(?P<command>(relative))                   # COMMANDS
        |
        (?P<open_brace>{) | (?P<close_brace>})      # { or }
    )
    """, 
    re.VERBOSE
)


def tokenize(s):
    while True:
        if s:
            m = token_pattern.match(s)
            if m:
                yield m.groupdict()
            else:
                raise Exception("unknown token at: '%s'" % s[:20])
            s = s[m.end():]
        else:
            raise StopIteration


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
    
    for token_dict in tokenize(s):
        command = token_dict["command"]
        open_brace = token_dict["open_brace"]
        close_brace = token_dict["close_brace"]
        tie = token_dict["tie"]
        
        if command:
            pass # @@@ NYI
        elif open_brace:
            pass # @@@ NYI
        elif close_brace:
            pass # @@@ NYI
        elif tie:
            pass # @@@ NYI
        else:
            note = token_dict["note"]
            octave_marker = token_dict["octave"]
            duration_marker = token_dict["duration"]
            accidental_sharp = token_dict["sharp"]
            accidental_flat = token_dict["flat"]
            rest = token_dict["rest"]
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
