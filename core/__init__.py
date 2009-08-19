# this is just an initial sketch of the data structures so don't read too 
# much into them at this stage.

# these are empty classes at the moment but are designed to eventually have
# extra methods on top of the str, list and dict types they extend


class Attribute(str):
    pass


class Sequence(list):
    pass


class Point(dict):
    pass


if __name__ == "__main__":
    
    OFFSET = Attribute("offset")
    PITCH = Attribute("pitch")
    DURATION = Attribute("duration")
    
    p1 = Point({
        OFFSET: 16,
        PITCH: 50,
        DURATION: 16,
    })
    
    p2 = Point({
        OFFSET: 32,
        PITCH: 52,
        DURATION: 16,
    })
    
    s1 = Sequence([p1, p2])
    
    assert s1 == [
        {'duration': 16, 'offset': 16, 'pitch': 50},
        {'duration': 16, 'offset': 32, 'pitch': 52}
    ]