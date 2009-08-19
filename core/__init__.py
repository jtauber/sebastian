# this is just an initial sketch of the data structures so don't read too 
# much into them at this stage.

# these are empty classes at the moment but are designed to eventually have
# extra methods on top of the str, list and dict types they extend


class Attribute(str):
    pass


class Sequence(list):
    pass


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