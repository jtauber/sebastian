
## graded tests derived from lilypond documentation that are likely to be relevant to In C implementation

# test (not written yet) takes two arguments. The first is a lilypond fragment. The second is the intended
# interpretation, a sequence of (offset, pitch, duration) tuples where offset and duration are in multiples of a 
# 64th note and pitch is MIDI note number.

# absolute octave entry

test(
    "c d e f g a b c d e f g",
    [
        (0, 48, 16), (16, 50, 16), (32, 52, 16), (48, 53, 16), (64, 55, 16), (80, 57, 16), (96, 59, 16),
        (112, 48, 16), (128, 50, 16), (144, 52, 16), (160, 53, 16), (176, 55, 16)
    ]
)

test(
    "c' c'' e' g d'' d' d c c, c,, e, g d,, d, d c",
    [
        (0, 60, 16), (16, 72, 16), (32, 64, 16), (48, 55, 16), (64, 74, 16), (80, 62, 16), (96, 50, 16),
        (112, 48, 16), (128, 36, 16), (144, 24, 16), (160, 38, 16), (176, 55, 16), (192, 26, 16), (208, 38, 16),
        (224, 50, 16), (240, 48, 16)
    ]
)


# duration

test(
    "a a a2 a a4 a a1 a",
    [
        (0, 69, 16), (16, 69, 16), (32, 69, 32), (64, 69, 32), (96, 69, 16), (112, 69, 16), (128, 69, 64),
        (192, 69, 64)
    ]
)

test(
    "a4 b c4. b8 a4. b4.. c8.",
    [
        (0, 69, 16), (16, 71, 16), (32, 72, 24), (56, 71, 8), (64, 69, 24), (88, 71, 28), (116, 72, 12)
    ]
)


# rests

test(
    "c4 r4 r8 c8 c4",
    [
        (0, 0, 0), (0, 0, 0), (0, 0, 0),
    ]
)

test(
    "r8 c d e",
    [
        (0, 0, 0), (0, 0, 0), (0, 0, 0),
    ]
)


# accidentals

test(
    "ais1 aes aisis aeses",
    [
        (0, 70, 16), (16, 68, 16), (32, 71, 16), (48, 67, 16)
    ]
)

test(
    "a4 aes a2",
    [
        (0, 69, 16), (16, 68, 16), (32, 69, 32)
    ]
)


# relative octave entry

test(
    r"\relative c { c d e f g a b c d e f g }",
    [
        (0, 48, 16), (16, 50, 16), (32, 52, 16), (48, 53, 16),
        (64, 55, 16), (80, 57, 16), (96, 59, 16), (112, 60, 16),
        (128, 62, 16), (144, 64, 16), (160, 65, 16), (176, 67, 16)
    ]
)

test(
    r"\relative c'' { c g c f, c' a, e'' c }",
    [
        (0, 72, 16), (16, 67, 16), (32, 72, 16), (48, 65, 16),
        (64, 72, 16), (80, 57, 16), (96, 76, 16), (112, 72, 16)
    ]
)

test(
    r"\relative c { c f b e a d g c }",
    [
        (0, 48, 16), (16, 53, 16), (32, 59, 16), (48, 64, 16),
        (64, 69, 16), (80, 74, 16), (96, 79, 16), (112, 84, 16)
    ]
)

test(
    r"\relative c'' { c2 fis c2 ges b2 eisis b2 feses }",
    [
        (0, 72, 32), (32, 78, 32), (64, 72, 32), (96, 66, 32),
        (128, 71, 32), (160, 78, 32), (192, 71, 32), (224, 63, 32)
    ]
)


# ties

test(
    "a2 ~ a",
    [
        (0, 57, 64)
    ]
)


# octave check

# test(
#     r"\relative c'' { c2 d='4 d e2 f }",
#     ...
# )


# acciaccatura

# test(
#     r"\acciaccatura d8 c4",
#     ...
# )
