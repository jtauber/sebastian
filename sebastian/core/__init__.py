# this is just an initial sketch of the data structures so don't read too
# much into them at this stage.

# basically, a Sequence is just a collection of Points and a Point is just a
# dict giving values to certain Attributes.
#
# there are three types of Sequences: OSequences, HSequences and VSequences
# only OSequences are currently implemented
#
# OSequence assumes the Points have OFFSET_64 attribute values and
# will also make use of the DURATION_64 attribute.
#
# see datastructure_notes.txt for some of the thinking behind this whole
# approach and a bit of roadmap as to where things are headed.


OFFSET_64 = "offset_64"
MIDI_PITCH = "midi_pitch"
DURATION_64 = "duration_64"
DEGREE = 'degree'

from sebastian.core.elements import OSeq, Point, VSeq, HSeq  # noqa

OSequence = OSeq(OFFSET_64, DURATION_64)

#
#
# def shift(offset):
#     def _(point):
#         point[OFFSET_64] = point[OFFSET_64] + offset
#         return point
#     return lambda seq: seq.map_points(_)
#
#
