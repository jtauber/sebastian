# this is just an initial sketch of the data structures so don't read too 
# much into them at this stage.

# basically, a Sequence is just a list of Points and a Point is just a dict
# giving values to certain Attributes.
#
# currently, Sequence assumes the Points have OFFSET_64 attribute values and
# will also make use of the DURATION_64 attribute. I'm not completely happy
# with this coupling but not sure how else to do it given Sequence needs to
# be offset aware.
#
# see datastructure_notes.txt for some of the thinking behind this whole
# approach and a bit of roadmap as to where things are headed.


# this str subclass exists as we may later add methods

class Attribute(str):
    pass


OFFSET_64 = Attribute("offset_64")
MIDI_PITCH = Attribute("midi_pitch")
DURATION_64 = Attribute("duration_64")


class Sequence(list):
    
    def __add__(self, next_seq):
        offset = self.next_offset()
        return Sequence(list.__add__(self, next_seq.offset_all(offset)))
    
    def __mul__(self, count):
        x = Sequence(self)
        for i in range(count - 1):
            x = x + Sequence(self)
        return x
    
    def last_point(self):
        if len(self) == 0:
            return Point({OFFSET_64: 0, DURATION_64: 0})
        else:
            return sorted(self, key=lambda x: x[OFFSET_64])[-1]
    
    def next_offset(self):
        point = self.last_point()
        return point[OFFSET_64] + point.get(DURATION_64, 0)
    
    def map(self, func):
        x = []
        for point in self:
            new_point = func(Point(point))
            x.append(new_point)
        return Sequence(x)
    
    def offset_all(self, offset):
        
        def _(point):
            point[OFFSET_64] = point[OFFSET_64] + offset
            return point
        
        return self.map(_)


class Point(dict):
    
    def tuple(self, *attributes):
        return tuple(self.get(attribute) for attribute in attributes)


# some mainline tests

if __name__ == "__main__":
    
    p1 = Point({
        OFFSET_64: 16,
        MIDI_PITCH: 50,
        DURATION_64: 16,
    })
    
    assert p1.tuple(OFFSET_64, DURATION_64) == (16, 16)
    
    p2 = Point({
        OFFSET_64: 32,
        MIDI_PITCH: 52,
        DURATION_64: 16,
    })
    
    s1 = Sequence([p1, p2])
    
    assert s1 == [
        {'duration_64': 16, 'offset_64': 16, 'midi_pitch': 50},
        {'duration_64': 16, 'offset_64': 32, 'midi_pitch': 52}
    ]
    
    assert s1 + s1 == [
        {'duration_64': 16, 'offset_64': 16, 'midi_pitch': 50},
        {'duration_64': 16, 'offset_64': 32, 'midi_pitch': 52},
        {'duration_64': 16, 'offset_64': 64, 'midi_pitch': 50},
        {'duration_64': 16, 'offset_64': 80, 'midi_pitch': 52}
    ]
    
    assert s1 * 2 == [
        {'duration_64': 16, 'offset_64': 16, 'midi_pitch': 50},
        {'duration_64': 16, 'offset_64': 32, 'midi_pitch': 52},
        {'duration_64': 16, 'offset_64': 64, 'midi_pitch': 50},
        {'duration_64': 16, 'offset_64': 80, 'midi_pitch': 52}
    ]
    
    assert s1 * 3 == [
        {'duration_64': 16, 'offset_64': 16, 'midi_pitch': 50},
        {'duration_64': 16, 'offset_64': 32, 'midi_pitch': 52},
        {'duration_64': 16, 'offset_64': 64, 'midi_pitch': 50},
        {'duration_64': 16, 'offset_64': 80, 'midi_pitch': 52},
        {'duration_64': 16, 'offset_64': 112, 'midi_pitch': 50},
        {'duration_64': 16, 'offset_64': 128, 'midi_pitch': 52}
    ]
