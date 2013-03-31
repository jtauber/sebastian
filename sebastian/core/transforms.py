from sebastian.core import MIDI_PITCH, OFFSET_64, DURATION_64
from sebastian.core import Point, OSequence

from sebastian.core.notes import modifiers, letter
from functools import wraps, partial


def transform_sequence(f):
    """
    A decorator to take a function operating on a point and
    turn it into a function returning a callable operating on a sequence.
    The functions passed to this decorator must define a kwarg called "point",
    or have point be the last positional argument
    """
    @wraps(f)
    def wrapper(*args, **kwargs):
        #The arguments here are the arguments passed to the transform,
        #ie, there will be no "point" argument

        #Send a function to seq.map_points with all of its arguments applied except
        #point
        return lambda seq: seq.map_points(partial(f, *args, **kwargs))

    return wrapper


@transform_sequence
def add(properties, point):
    point.update(properties)
    return point


@transform_sequence
def degree_in_key(key, point):
    degree = point["degree"]
    pitch = key.degree_to_pitch(degree)
    point["pitch"] = pitch
    return point


@transform_sequence
def degree_in_key_with_octave(key, base_octave, point):
    degree = point["degree"]
    pitch, octave = key.degree_to_pitch_and_octave(degree)
    point["pitch"] = pitch
    point["octave"] = octave + base_octave
    return point


#TODO: make a converter from semitones, so that you can easily
#transpose by a number of semitones
@transform_sequence
def transpose(interval, point):
    """
    Transpose a point by an interval, using the Sebastian interval system
    """
    if "pitch" in point:
        point["pitch"] = point["pitch"] + interval
    return point


@transform_sequence
def stretch(multiplier, point):
    point[OFFSET_64] = int(point[OFFSET_64] * multiplier)
    if DURATION_64 in point:
        point[DURATION_64] = int(point[DURATION_64] * multiplier)
    return point


@transform_sequence
def invert(midi_pitch_pivot, point):
    if MIDI_PITCH in point:
        interval = point[MIDI_PITCH] - midi_pitch_pivot
        point[MIDI_PITCH] = midi_pitch_pivot - interval
    return point


def reverse():
    def _(sequence):
        new_elements = []
        last_offset = sequence.next_offset()
        if sequence and sequence[0][OFFSET_64] != 0:
            old_sequence = OSequence([Point({OFFSET_64: 0})]) + sequence
        else:
            old_sequence = sequence
        for point in old_sequence:
            new_point = Point(point)
            new_point[OFFSET_64] = last_offset - new_point[OFFSET_64] - new_point.get(DURATION_64, 0)
            if new_point != {OFFSET_64: 0}:
                new_elements.append(new_point)
        return OSequence(sorted(new_elements, key=lambda x: x[OFFSET_64]))
    return _


def subseq(start_offset=0, end_offset=None):
    """
    Return a portion of the input sequence
    """
    def _(sequence):
        return sequence.subseq(start_offset, end_offset)
    return _


@transform_sequence
def midi_pitch(point):
    octave = point["octave"]
    pitch = point["pitch"]
    midi_pitch = [2, 9, 4, 11, 5, 0, 7][pitch % 7]
    midi_pitch += modifiers(pitch)
    midi_pitch += 12 * octave
    point[MIDI_PITCH] = midi_pitch
    return point


@transform_sequence
def midi_to_pitch(point):  # @@@ add key hint later
    if MIDI_PITCH not in point:
        return point
    midi_pitch = point[MIDI_PITCH]

    octave, pitch = divmod(midi_pitch, 12)
    pitch = [-2, 5, 0, -5, 2, -3, 4, -1, 6, 1, -4, 3][pitch]

    point["octave"] = octave
    point["pitch"] = pitch

    return point


@transform_sequence
def lilypond(point):
    """
    Generate lilypond representation for a point
    """
    #If lilypond already computed, leave as is
    if "lilypond" in point:
        return point

    #Defaults:
    pitch_string = ""
    octave_string = ""
    duration_string = ""
    preamble = ""
    dynamic_string = ""
    if "pitch" in point:
        octave = point["octave"]
        pitch = point["pitch"]
        if octave > 4:
            octave_string = "'" * (octave - 4)
        elif octave < 4:
            octave_string = "," * (4 - octave)
        else:
            octave_string = ""
        m = modifiers(pitch)
        if m > 0:
            modifier_string = "is" * m
        elif m < 0:
            modifier_string = "es" * -m
        else:
            modifier_string = ""
        pitch_string = letter(pitch).lower() + modifier_string

    if DURATION_64 in point:
        duration = point[DURATION_64]
        if duration > 0:
            if duration % 3 == 0:  # dotted note
                duration_string = str(192 // (2 * duration)) + "."
            else:
                duration_string = str(64 // duration)
        #TODO: for now, if we have a duration but no pitch, show a 'c' with an x note
        if duration_string:
            if not pitch_string:
                pitch_string = "c"
                octave_string = "'"
                preamble = r'\xNote '

    if "dynamic" in point:
        dynamic = point["dynamic"]
        if dynamic == "crescendo":
            dynamic_string = "\<"
        elif dynamic == "diminuendo":
            dynamic_string = "\>"
        else:
            dynamic_string = "\%s" % (dynamic,)

    point["lilypond"] = "%s%s%s%s%s" % (preamble, pitch_string, octave_string, duration_string, dynamic_string)

    return point

_dynamic_markers_to_velocity = {
    "pppppp": 10,
    "ppppp": 16,
    "pppp": 20,
    "ppp": 24,
    "pp": 36,
    "p": 48,
    "mp": 64,
    "mf": 74,
    "f": 84,
    "ff": 94,
    "fff": 114,
    "ffff": 127,
}


def dynamics(start, end=None):
    """
    Apply dynamics to a sequence. If end is specified, it will crescendo or diminuendo linearly from start to end dynamics.

    You can pass any of these strings as dynamic markers: ['pppppp', 'ppppp', 'pppp', 'ppp', 'pp', 'p', 'mp', 'mf', 'f', 'ff', 'fff', ''ffff]

    Args:
        start: beginning dynamic marker, if no end is specified all notes will get this marker
        end: ending dynamic marker, if unspecified the entire sequence will get the start dynamic marker

    Example usage:

        s1 | dynamics('p')  # play a sequence in piano
        s2 | dynamics('p', 'ff')  # crescendo from p to ff
        s3 | dynamics('ff', 'p')  # diminuendo from ff to p
    """
    def _(sequence):
        if start in _dynamic_markers_to_velocity:
            start_velocity = _dynamic_markers_to_velocity[start]
            start_marker = start
        else:
            raise ValueError("Unknown start dynamic: %s, must be in %s" % (start, _dynamic_markers_to_velocity.keys()))

        if end is None:
            end_velocity = start_velocity
            end_marker = start_marker
        elif end in _dynamic_markers_to_velocity:
            end_velocity = _dynamic_markers_to_velocity[end]
            end_marker = end
        else:
            raise ValueError("Unknown end dynamic: %s, must be in %s" % (start, _dynamic_markers_to_velocity.keys()))

        retval = sequence.__class__([Point(point) for point in sequence._elements])

        velocity_interval = (float(end_velocity) - float(start_velocity)) / (len(retval) - 1) if len(retval) > 1 else 0
        velocities = [int(start_velocity + velocity_interval * pos) for pos in range(len(retval))]

        # insert dynamics markers for lilypond
        if start_velocity > end_velocity:
            retval[0]["dynamic"] = "diminuendo"
            retval[-1]["dynamic"] = end_marker
        elif start_velocity < end_velocity:
            retval[0]["dynamic"] = "crescendo"
            retval[-1]["dynamic"] = end_marker
        else:
            retval[0]["dynamic"] = start_marker

        for point, velocity in zip(retval, velocities):
            point["velocity"] = velocity

        return retval
    return _
