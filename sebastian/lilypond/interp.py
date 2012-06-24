from sebastian.core import OSequence, Point, OFFSET_64, MIDI_PITCH, DURATION_64

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
                ((?P<sharp>(is)+)|(?P<flat>(es)+)) ?    # ACCIDENTALS ?
                (?P<octave>'+|,+) ?                     # OCTAVE ?
                (=(?P<octave_check>'+|,+)) ?            # OCTAVE CHECK ?
                |                                       # or
                (?P<rest>r)                             # REST
            )
            (?P<duration>\d+\.*) ?                      # DURATION ?
            (\s*(?P<tie>~)) ?                           # TIE ?
        )
        |                                           # or
        \\(?P<command>(                             # COMMANDS
            relative | acciaccatura
        ))
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


def note_tuple(token_dict, relative_note_tuple=None):
    note = token_dict["note"]
    octave_marker = token_dict["octave"]
    octave_check = token_dict["octave_check"]
    accidental_sharp = token_dict["sharp"]
    accidental_flat = token_dict["flat"]
    accidental_change = 0
    
    if relative_note_tuple:
        prev_note, prev_accidental_change, prev_octave = relative_note_tuple
        
        diff = MIDI_NOTE_VALUES[note] - prev_note
        if diff >= 7:
            base_octave = prev_octave - 1
        elif diff <= -7:
            base_octave = prev_octave + 1
        else:
            base_octave = prev_octave
    else:
        base_octave = 4
    
    if octave_marker is None:
        octave = base_octave
    elif "'" in octave_marker:
        octave = base_octave + len(octave_marker)
    elif "," in octave_marker:
        octave = base_octave - len(octave_marker)
    if accidental_sharp:
        accidental_change += len(accidental_sharp) / 2
    if accidental_flat:
        accidental_change -= len(accidental_flat) / 2
    
    if octave_check is None:
        pass
    elif "'" in octave_check:
        correct_octave = 4 + len(octave_check)
        if octave != correct_octave:
            print "WARNING: failed octave check" # @@@ better reporting of warning
            octave = correct_octave
    elif "," in octave_check:
        correct_octave = 4 - len(octave_check)
        if octave != correct_octave:
            print "WARNING: failed octave check" # @@@ better reporting of warning
            octave = correct_octave
    
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
    
    duration = int((2 - (2**-dots)) * 64 / core)
    
    return duration


def process_note(token_dict, relative_mode, prev_note_tuple):
    # @@@ there is still code duplication between here and the main parsing
    # further on
    # @@@ some of the args passed in above could be avoided if this and
    # parse_block were methods on a class
    
    duration_marker = token_dict["duration"]
    # duration must be explicit
    duration = parse_duration(duration_marker)
    
    if relative_mode:
        note_base, accidental_change, octave = note_tuple(token_dict, relative_note_tuple=prev_note_tuple)
    else:
        note_base, accidental_change, octave = note_tuple(token_dict)
    
    note_value = note_base + (12 * octave) + accidental_change
    
    return note_value, duration


def parse_block(token_generator, prev_note_tuple=None, relative_mode=False, offset=0):
    prev_duration = 16
    tie_deferred = False
    
    try:
        while True:
            token_dict = token_generator.next()
            
            command = token_dict["command"]
            open_brace = token_dict["open_brace"]
            close_brace = token_dict["close_brace"]
            
            if command:
                if command == "relative":
                    
                    token_dict = token_generator.next()
                    
                    base_note_tuple = note_tuple(token_dict)
                    
                    token_dict = token_generator.next()
                    if not token_dict["open_brace"]:
                        raise Exception("\\relative must be followed by note then {...} block")
                    
                    for obj in parse_block(token_generator, prev_note_tuple=base_note_tuple, relative_mode=True, offset=offset):
                        yield obj
                        last_offset = obj[OFFSET_64]
                    offset = last_offset
                elif command == "acciaccatura":
                    # @@@ there is much code duplication between here and the
                    # main parsing further on
                    
                    token_dict = token_generator.next()
                    note_value, duration = process_note(token_dict, relative_mode, prev_note_tuple)
                    yield Point({OFFSET_64: offset - duration / 2, MIDI_PITCH: note_value, DURATION_64: duration / 2})
                    
                    token_dict = token_generator.next()
                    note_value, duration = process_note(token_dict, relative_mode, prev_note_tuple)
                    yield Point({OFFSET_64: offset, MIDI_PITCH: note_value, DURATION_64: duration})
                    
                    offset += duration
                    prev_duration = duration
                    
                    # @@@ this should be uncommented but I'll wait until a
                    # unit test proves it should be uncommented!
                    # prev_note_tuple = note_base, accidental_change, octave
                    
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
                    if relative_mode:
                        note_base, accidental_change, octave = note_tuple(token_dict, relative_note_tuple=prev_note_tuple)
                    else:
                        note_base, accidental_change, octave = note_tuple(token_dict)
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
                        yield Point({OFFSET_64: offset, MIDI_PITCH: note_value, DURATION_64: duration})
                    
                    prev_note_tuple = note_base, accidental_change, octave
                
                if not tie_deferred:
                    offset += duration
                
                prev_duration = duration
    except StopIteration:
        yield Point({OFFSET_64: offset})
        raise StopIteration


def parse(s, offset=0):
    return OSequence(list(parse_block(tokenize(s), offset=offset)))
