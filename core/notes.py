# line of fifths with D at origin
#
# ... Fbb Cbb Gbb Dbb Abb Ebb Bbb Fb  Cb  Gb  Db  Ab  Eb  Bb  F   C   G   D
#     -17 -16 -15 -14 -13 -12 -11 -10 -9  -8  -7  -6  -5  -4  -3  -2  -1  0
#
# D   A   E   B   F#  C#  G#  D#  A#  E#  B#  Fx  Cx  Gx  Dx  Ax  Ex  Bx  ...
# 0   +1  +2  +3  +4  +5  +6  +7  +8  +9  +10 +11 +12 +13 +14 +15 +16 +17

def natural(val):
    return abs(val) < 4

def single_sharp(val):
    return 3 < val < 11

def single_flat(val):
    return -3 > val > -11

def double_sharp(val):
    return 10 < val < 18

def double_flat(val):
    return -10 > val > -18

def modifiers(val):
    return ((val + 3) - ((val + 3) % 7)) / 7

def mod_interval(mod):
    return 7 * mod

def letter(val):
    return "DAEBFCG"[val % 7]

def name(val):
    m = modifiers(val)
    if m == 0:
        m_name = ""
    elif m == 1:
        m_name = "#"
    elif m > 1:
        m_name = "x" * (m - 1)
    else: # m < 0
        m_name = "b" * -m
    return letter(val) + m_name

def value(name):
    letter = name[0]
    base = "FCGDAEB".find(letter) - 3
    if base == -4:
        raise ValueError
    mod = name[1:]
    if mod == "":
        m = 0
    elif mod == "#":
        m = 1
    elif mod == "x" * len(mod):
        m = len(mod) + 1
    elif mod == "b" * len(mod):
        m = -len(mod)
    else:
        raise ValueError
    return base + mod_interval(m)

# tone above, new letter
def tone_above(val): 
    return val + 2

# tone below, new letter
def tone_below(val): 
    return val - 2

# semitone above, new letter
def semitone_above(val): 
    return val - 5

# semitone above, new letter
def semitone_below(val): 
    return val + 5

# semitone above, same letter
def augment(val):
    return val + 7
    
# semitone below, same latter
def diminish(val):
    return val - 7

def enharmonic(val1, val2):
    return (abs(val1 - val2) % 12) == 0

# major scale

def major_scale(tonic):
    return [tonic + i for i in [0, 2, 4, -1, 1, 3, 5]]

def minor_scale(tonic):
    return [tonic + i for i in [0, 2, -3, -1, 1, -4, -2]]


class Key:
    def __init__(self, tonic, scale):
        self.notes = scale(value(tonic))
    
    def degree_to_pitch(self, degree):
        return self.notes[degree - 1]
    
    def degree_to_pitch_and_octave(self, degree):
        o, d = divmod(degree - 1, 7)
        return self.notes[d], o


## TESTS

if __name__ == "__main__":
    assert natural(-3)
    assert natural(2)
    assert natural(0)
    assert not natural(-4)
    assert not natural(5)
    
    assert not single_sharp(0)
    assert not single_sharp(-5)
    assert single_sharp(4)
    assert not single_sharp(12)
    
    assert modifiers(0) == 0
    assert modifiers(2) == 0
    assert modifiers(-1) == 0
    assert modifiers(-5) == -1
    assert modifiers(-11) == -2
    assert modifiers(-17) == -2
    assert modifiers(4) == 1
    assert modifiers(13) == 2
    assert modifiers(17) == 2
    
    assert value("G#") == 6
    
    print [name(x) for x in major_scale(value("G#"))]
