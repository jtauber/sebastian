from unittest import TestCase


class TestWriteMidi(TestCase):

    def test_write_midi(self):
        """
        Writing out test.mid to ensure midi processing works.

        This isn't really a test.
        """
        from sebastian.core import OSequence, Point
        from sebastian.core import OFFSET_64, MIDI_PITCH, DURATION_64
        test = OSequence([
            Point({OFFSET_64: o, MIDI_PITCH: m, DURATION_64: d}) for (o, m, d) in [
                (0, 60, 16), (16, 72, 16), (32, 64, 16), (48, 55, 16),
                (64, 74, 16), (80, 62, 16), (96, 50, 16), (112, 48, 16),
                (128, 36, 16), (144, 24, 16), (160, 40, 16), (176, 55, 16),
                (192, 26, 16), (208, 38, 16), (224, 50, 16), (240, 48, 16)
            ]
        ])

        from sebastian.midi.write_midi import write
        write("test.mid", [test])
