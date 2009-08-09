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
                |                                       # or
                (?P<rest>r)                             # REST
            )
            (?P<duration>\d+\.*) ?                      # DURATION ?
            (\s*(?P<tie>~)) ?                           # TIE ?
        )
        |                                           # or
        \\(?P<command>(relative))                   # COMMANDS
        |                                           # or
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


def absolute_note_value(token_dict):
    note = token_dict["note"]
    octave_marker = token_dict["octave"]
    accidental_sharp = token_dict["sharp"]
    accidental_flat = token_dict["flat"]
    accidental_change = 0
    
    if octave_marker is None:
        octave = 4
    elif "'" in octave_marker:
        octave = 4 + len(octave_marker)
    elif "," in octave_marker:
        octave = 4 - len(octave_marker)
    if accidental_sharp:
        accidental_change += len(accidental_sharp) / 2
    if accidental_flat:
        accidental_change -= len(accidental_flat) / 2
    
    return MIDI_NOTE_VALUES[note], accidental_change, octave


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


def parse_block(token_generator, prev_note_tuple = None, relative_mode = False, offset = 0):
    prev_duration = 16
    tie_deferred = False
    
    while True:
        token_dict = token_generator.next()
        
        command = token_dict["command"]
        open_brace = token_dict["open_brace"]
        close_brace = token_dict["close_brace"]
        
        if command:
            pass # @@@ NYI
        elif open_brace:
            for obj in parse_block(token_generator):
                yield obj
        elif close_brace:
            raise StopIteration
        else:
            duration_marker = token_dict["duration"]
            rest = token_dict["rest"]
            tie = token_dict["tie"]
            
            if duration_marker is None:
                duration = prev_duration
            else:
                duration = parse_duration(duration_marker)
            
            if not rest:
                note_base, accidental_change, octave = absolute_note_value(token_dict)
                note_value = note_base + (12 * octave) + accidental_change
                
                if tie_deferred:
                    # if the previous note was deferred due to a tie
                    prev_note_value = prev_note_tuple[0] + (12 * prev_note_tuple[2]) + prev_note_tuple[1]
                    if note_value != prev_note_value:
                        raise Exception("ties are only supported between notes of same pitch")
                    duration += prev_duration
                    tie_deferred = False
                
                if tie:
                    # if there is a tie following this note, we defer it
                    tie_deferred = True
                else:
                    yield (offset, note_value, duration)
                
                prev_note_tuple = note_base, accidental_change, octave
            
            if not tie_deferred:
                offset += duration
            
            prev_duration = duration


def parse(s):
    return parse_block(tokenize(s))
