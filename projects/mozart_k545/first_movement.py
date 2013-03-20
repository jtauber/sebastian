"""
This script will build up the first movement of Mozart's C major Sonata (K545)
while trying out experimental features of Sebastian.
"""
from pprint import pprint
from sebastian.core import Point, HSeq, VSeq, OSequence, DURATION_64, DEGREE
from sebastian.core.transforms import midi_pitch, degree_in_key_with_octave, add, transform_sequence
from sebastian.core.notes import Key, major_scale
from sebastian.midi import write_midi


def transpose_degree(point, degree_delta):
    result = Point(point)
    result[DEGREE] = result[DEGREE] + degree_delta
    return result


@transform_sequence
def chord(point):
    children = [transpose_degree(point, i) for i in point.get('chord', (0, 2, 4))]
    point["sequence"] = VSeq(children)
    return point


@transform_sequence
def arpeggio(pattern, point):
    """
    turns each subsequence into an arpeggio matching the given ``pattern``.
    """
    point['sequence'] = HSeq(point['sequence'][i] for i in pattern)
    return point


@transform_sequence
def fill(duration, point):
    """
    fills the subsequence of the point with repetitions of its subsequence and
    sets the ``duration`` of each point.
    """
    point['sequence'] = point['sequence'] * (point[DURATION_64] / (8 * duration)) | add({DURATION_64: duration})
    return point


def expand(sequence):
    """
    expands a tree of sequences into a single, flat sequence, recursively.
    """
    expanse = []
    for point in sequence:
        if 'sequence' in point:
            expanse.extend(expand(point['sequence']))
        else:
            expanse.append(point)
    return sequence.__class__(expanse)


def debug(sequence):
    """
    adds information to the sequence for better debugging, currently only 
    an index property on each point in the sequence.
    """
    points = []
    for i, p in enumerate(sequence):
        copy = Point(p)
        copy['index'] = i
        points.append(copy)
    return sequence.__class__(points)


def build_movement():
    # Define our alberti bass signature.
    alberti = arpeggio([0, 2, 1, 2])

    # Create the basic interval pattern.
    intervals = HSeq({DEGREE: x} for x in [1, 5, 1, 4, 1, 5, 1])

    # Create the rhythm
    rhythm = HSeq({DURATION_64: x} for x in [128, 64, 64, 64, 64, 64, 64])

    # Set specific chords to be used in certain measures.
    intervals[1]["chord"] = (-3, -1, 0, 2)  # second inversion 7th
    intervals[3]["chord"] = (-3, 0, 2)      # second inversion
    intervals[5]["chord"] = (-5, -3, 0)     # first inversion

    # Combine the sequences, make them chords, produce alberti on the chords, 
    # fill with each being 8, expand it to a flat sequence.
    melody = intervals & rhythm | chord() | alberti | fill(8) | expand

    # Define our key
    C_major = Key("C", major_scale)

    #key(major_scale(-2))

    # Set the degree, add the midi pitch, make it an OSequence, add debugging information.
    return melody | degree_in_key_with_octave(C_major, 5) | midi_pitch() | OSequence | debug


if __name__ == "__main__":
    movement = build_movement()
    for point in movement:
        pprint(point)
    write_midi.write("first_movement.mid", [movement])
