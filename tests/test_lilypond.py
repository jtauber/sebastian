from unittest import TestCase

## graded tests derived from lilypond documentation that are likely to be
## relevant to In C implementation

from sebastian.core import OFFSET_64, MIDI_PITCH, DURATION_64
from sebastian.lilypond.interp import parse


class TestLilyPond(TestCase):

    def eq(self, lilypond, answer):
        """ The first is a lilypond fragment. The second is
        the intended interpretation, a sequence of (offset, pitch, duration) tuples
        where offset and duration are in multiples of a 64th note and pitch is MIDI
        note number.
        """

        print "\nTEST: %s" % lilypond
        result = parse(lilypond)
        i = -1  # so available in else clause of for
        for i, event in enumerate(answer):
            r = result[i].tuple(OFFSET_64, MIDI_PITCH, DURATION_64)
            if event != r:
                print "%s != %s" % (event, r)
                assert False, "\x1B[31mFAIL\x1B[0m"
                break
            else:
                print "%s == %s" % (event, r)
        else:
            if len(answer) != len(result):
                assert False, "\x1B[31mFAIL (different length)\x1B[0m"
                for j in range(i + 1, len(result)):
                    print "!= %s" % (result[j].tuple(OFFSET_64, MIDI_PITCH, DURATION_64), )
            else:
                print "\x1B[32mSUCCESS\x1B[0m"

    def test_absolute_octave_entry(self):
        self.eq(
            "c d e f g a b c d e f g",
            [
                (0, 48, 16), (16, 50, 16), (32, 52, 16), (48, 53, 16),
                (64, 55, 16), (80, 57, 16), (96, 59, 16), (112, 48, 16),
                (128, 50, 16), (144, 52, 16), (160, 53, 16), (176, 55, 16),
                (192, None, None),
            ]
        )

        self.eq(
            "c' c'' e' g d'' d' d c c, c,, e, g d,, d, d c",
            [
                (0, 60, 16), (16, 72, 16), (32, 64, 16), (48, 55, 16),
                (64, 74, 16), (80, 62, 16), (96, 50, 16), (112, 48, 16),
                (128, 36, 16), (144, 24, 16), (160, 40, 16), (176, 55, 16),
                (192, 26, 16), (208, 38, 16), (224, 50, 16), (240, 48, 16),
                (256, None, None),
            ]
        )

    def test_duration(self):
        self.eq(
            "a a a2 a a4 a a1 a",
            [
                (0, 57, 16), (16, 57, 16), (32, 57, 32), (64, 57, 32),
                (96, 57, 16), (112, 57, 16), (128, 57, 64), (192, 57, 64),
                (256, None, None),
            ]
        )

    def test_more_durations(self):
        self.eq(
            "a4 b c4. b8 a4. b4.. c8.",
            [
                (0, 57, 16), (16, 59, 16), (32, 48, 24), (56, 59, 8),
                (64, 57, 24), (88, 59, 28), (116, 48, 12),
                (128, None, None),
            ]
        )

    def test_rests(self):

        self.eq(
            "c4 r4 r8 c8 c4",
            [
                (0, 48, 16), (40, 48, 8), (48, 48, 16),
                (64, None, None),
            ]
        )

        self.eq(
            "r8 c d e",
            [
                (8, 48, 8), (16, 50, 8), (24, 52, 8),
                (32, None, None),
            ]
        )

    def test_accidentals(self):
        self.eq(
            "ais1 aes aisis aeses",
            [
                (0, 58, 64), (64, 56, 64), (128, 59, 64), (192, 55, 64),
                (256, None, None),
            ]
        )

        self.eq(
            "a4 aes a2",
            [
                (0, 57, 16), (16, 56, 16), (32, 57, 32),
                (64, None, None),
            ]
        )

    def test_relative_octave_entry(self):

        self.eq(
            r"\relative c { c d e f g a b c d e f g }",
            [
                (0, 48, 16), (16, 50, 16), (32, 52, 16), (48, 53, 16),
                (64, 55, 16), (80, 57, 16), (96, 59, 16), (112, 60, 16),
                (128, 62, 16), (144, 64, 16), (160, 65, 16), (176, 67, 16),
                (192, None, None),
                (192, None, None),
            ]
        )

        self.eq(
            r"\relative c'' { c g c f, c' a, e'' c }",
            [
                (0, 72, 16), (16, 67, 16), (32, 72, 16), (48, 65, 16),
                (64, 72, 16), (80, 57, 16), (96, 76, 16), (112, 72, 16),
                (128, None, None),
                (128, None, None),
            ]
        )

        self.eq(
            r"\relative c { c f b e a d g c }",
            [
                (0, 48, 16), (16, 53, 16), (32, 59, 16), (48, 64, 16),
                (64, 69, 16), (80, 74, 16), (96, 79, 16), (112, 84, 16),
                (128, None, None),
                (128, None, None),
            ]
        )

        self.eq(
            r"\relative c'' { c2 fis c2 ges b2 eisis b2 feses }",
            [
                (0, 72, 32), (32, 78, 32), (64, 72, 32), (96, 66, 32),
                (128, 71, 32), (160, 78, 32), (192, 71, 32), (224, 63, 32),
                (256, None, None),
                (256, None, None),
            ]
        )

    def test_ties(self):
        self.eq(
            "a2 ~ a",
            [
                (0, 57, 64),
                (64, None, None),
            ]
        )

    def test_octave_check(self):
        import logging
        logging.disable(logging.WARN)
        self.eq(
            r"\relative c'' { c2 d='4 d e2 f }",
            [
                (0, 72, 32), (32, 62, 16), (48, 62, 16), (64, 64, 32), (96, 65, 32),
                (128, None, None),
                (128, None, None),
            ]
        )
        logging.disable(logging.NOTSET)

    def test_acciaccatura(self):
        self.eq(
            r"\acciaccatura d8 c4",
            [
                (-4, 50, 4), (0, 48, 16),
                (16, None, None),
            ]
        )

    def test_for_regression_of_a_bug_in_ordering_of_accidental_and_octave(self):
        self.eq(
            "fis'",
            [
                (0, 66, 16),
                (16, None, None),
            ]
        )
