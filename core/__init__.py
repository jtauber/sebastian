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


# this str subclass exists as we may later add methods

class Attribute(str):
    pass


OFFSET_64 = Attribute("offset_64")
MIDI_PITCH = Attribute("midi_pitch")
DURATION_64 = Attribute("duration_64")


def shift(offset):
    def _(point):
        point[OFFSET_64] = point[OFFSET_64] + offset
        return point
    return lambda seq: seq.map_points(_)


class Point(dict):
    
    def tuple(self, *attributes):
        return tuple(self.get(attribute) for attribute in attributes)


class SequenceBase(object):
    """
    abstract base class of the different sequence types
    """
    
    def __init__(self, elements):
        self.elements = elements
    
    def to_list(self):
        return self.elements
    
    def __getitem__(self, item):
        return self.elements[item]
    
    def map_points(self, func):
        return self.__class__([func(Point(point)) for point in self.elements])
    
    
    ## operations
    
    def transform(self, func):
        """
        applies function to a sequence to produce a new sequence
        """
        
        # @@@ should this assume func will do the copying
        return func(self)
    
    
    ## operator overloading
    
    __or__ = transform


class OSequence(SequenceBase):
    """
    a sequence with OFFSET_64 attributes indicating offsets.
    """
    
    ## utility methods
    
    def last_point(self):
        if len(self.elements) == 0:
            return Point({OFFSET_64: 0, DURATION_64: 0})
        else:
            return sorted(self.elements, key=lambda x: x[OFFSET_64])[-1]
    
    def next_offset(self):
        point = self.last_point()
        return point[OFFSET_64] + point.get(DURATION_64, 0)
    
    def append(self, point):
        point = Point(point)
        point[OFFSET_64] = self.next_offset()
        self.elements.append(point)
    
    
    ## operations
    
    def concatenate(self, next_seq):
        """
        concatenates two sequences to produce a new sequence
        """
        
        offset = self.next_offset()
        
        return OSequence(self.elements + (next_seq | shift(offset)).elements)
    
    def repeat(self, count):
        """
        repeat sequence given number of times to produce a new sequence
        """
        
        x = OSequence([])
        for i in range(count):
            x = x.concatenate(self)
        return x
    
    def merge(self, parallel_seq):
        """
        combine the points in two sequences, putting them in offset order
        """
        
        return OSequence(sorted(self.elements + parallel_seq.elements, key=lambda x: x.get(OFFSET_64, 0)))
    
    
    def __eq__(self, other):
        return self.elements == other.elements
    
    
    ## operator overloading
    
    __add__ = concatenate
    __mul__ = repeat
    __floordiv__ = merge


class HSequence(SequenceBase):
    """
    a horizontal sequence where each element follows the previous
    """
    
    def to_osequence(self):
        x = OSequence([])
        for element in self.elements:
            x.append(element)
        return x
    
    
    ## operations
    
    def concatenate(self, next_seq):
        """
        concatenates two sequences to produce a new sequence
        """
        
        return HSequence(self.elements + next_seq.elements)
    
    def repeat(self, count):
        """
        repeat sequence given number of times to produce a new sequence
        """
        
        x = HSequence([])
        for i in range(count):
            x = x.concatenate(self)
        return x
    
    def __eq__(self, other):
        return self.elements == other.elements
    
    
    ## operator overloading
    
    __add__ = concatenate
    __mul__ = repeat


class VSequence(SequenceBase):
    """
    a vertical sequence where each element is coincident with the others
    """
    
    ## operations
    
    def merge(self, parallel_seq):
        """
        combine the points in two sequences, putting them in offset order
        """
        
        return VSequence(self.elements + parallel_seq.elements)
    
    
    def __eq__(self, other):
        return self.elements == other.elements
    
    
    ## operator overloading
    
    __floordiv__ = merge
