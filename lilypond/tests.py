
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
    ...
)


# duration

test(
    "a a a2 a a4 a a1 a",
    ...
)

test(
    "a4 b c4. b8 a4. b4.. c8.",
    ...
)


# rests

# @@@


# accidentals

test(
    "ais1 aes aisis aeses",
    ...
)

test(
    "a4 aes a2",
    ...
)


# relative octave entry

test(
    r"\relative c { c d e f g a b c d e f g }",
    ...
)

test(
    r"\relative c'' { c g c f, c' a, e'' c }",
    ...
)

test(
    r"\relative c { c f b e a d g c }",
    ...
)

test(
    r"\relative c'' { c2 fis c2 ges b2 eisis b2 feses }",
    ...
)


# ties

test(
    "a2 ~ a",
    ...
)


# octave check

test(
    r"\relative c'' { c2 d='4 d e2 f }",
    ...
)


# acciaccatura

test(
    r"\acciaccatura d8 c4",
    ...
)
