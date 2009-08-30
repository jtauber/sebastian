# this is just an initial sketch of the data structures so don't read too 
# much into them at this stage.

# these are empty classes at the moment but are designed to eventually have
# extra methods on top of the str, list and dict types they extend


class Attribute(str):
    pass


class Sequence(list):
    
    def __add__(self, next_seq):
        l = self.last_offset()
        return Sequence(list.__add__(self, next_seq.offset_all(l)))
    
    def __mul__(self, count):
        x = Sequence(self)
        for i in range(count - 1):
            x = x + Sequence(self)
        return x
    
    def last_offset(self):
        if len(self) == 0:
            return 0
        last_point = sorted(self, key=lambda x: x[OFFSET_64])[-1]
        return last_point[OFFSET_64] + last_point.get(DURATION_64, 0)
    
    def offset_all(self, offset):
        x = []
        for point in self:
            new_point = Point(point)
            new_point[OFFSET_64] = new_point[OFFSET_64] + offset
            x.append(new_point)
        return Sequence(x)


class Point(dict):
    
    def tuple(self, *attributes):
        return tuple(self.get(attribute) for attribute in attributes)


OFFSET_64 = Attribute("offset_64")
MIDI_PITCH = Attribute("midi_pitch")
DURATION_64 = Attribute("duration_64")


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
