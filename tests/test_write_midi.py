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

        from sebastian.midi.write_midi import SMF
        from io import BytesIO
        out_fd = BytesIO(bytearray())

        expected_bytes = b'MThd\x00\x00\x00\x06\x00\x01\x00\x02\x00\x10MTrk\x00\x00\x00%\x00\xffX\x04\x04\x02\x18\x08\x00\xffY\x02\x00\x00\x00\xffQ\x03\x07\xa1 \x00\xff\x03\x08untitled\x00\xff/\x00MTrk\x00\x00\x00\x87\x00\xc0\x00\x00\x90<@\x10\x80<\x00\x00\x90H@\x10\x80H\x00\x00\x90@@\x10\x80@\x00\x00\x907@\x10\x807\x00\x00\x90J@\x10\x80J\x00\x00\x90>@\x10\x80>\x00\x00\x902@\x10\x802\x00\x00\x900@\x10\x800\x00\x00\x90$@\x10\x80$\x00\x00\x90\x18@\x10\x80\x18\x00\x00\x90(@\x10\x80(\x00\x00\x907@\x10\x807\x00\x00\x90\x1a@\x10\x80\x1a\x00\x00\x90&@\x10\x80&\x00\x00\x902@\x10\x802\x00\x00\x900@\x10\x800\x00\x00\xff/\x00'

        s = SMF([test], instruments=None)
        s.write(out_fd)
        actual_bytes = out_fd.getvalue()

        self.assertEqual(expected_bytes, actual_bytes)

    def test_write_midi_multi_tacks(self):
        """
        Writing out test.mid to ensure midi processing works.

        This isn't really a test.
        """
        from sebastian.core import OSequence, Point
        from sebastian.core import OFFSET_64, MIDI_PITCH, DURATION_64
        test1 = OSequence([
            Point({OFFSET_64: o, MIDI_PITCH: m, DURATION_64: d}) for (o, m, d) in [
                (0, 60, 16), (16, 72, 16), (32, 64, 16), (48, 55, 16),
            ]
        ])
        test2 = OSequence([
            Point({OFFSET_64: o, MIDI_PITCH: m, DURATION_64: d}) for (o, m, d) in [
                (0, 55, 16), (16, 55, 16), (32, 64, 16), (48 + 16, 55, 16 * 10),
            ]
        ])

        from sebastian.midi.write_midi import SMF
        from io import BytesIO
        out_fd = BytesIO(bytearray())

        expected_bytes = b"""MThd\x00\x00\x00\x06\x00\x01\x00\x03\x00\x10MTrk\x00\x00\x00&\x00\xffX\x04\x04\x02\x18\x08\x00\xffY\x02\x00\x00\x00\xffQ\x03\x07\xa1 \x00\xff\x03\ttest song\x00\xff/\x00MTrk\x00\x00\x00'\x00\xc0\x00\x00\x90<@\x10\x80<\x00\x00\x90H@\x10\x80H\x00\x00\x90@@\x10\x80@\x00\x00\x907@\x10\x807\x00\x00\xff/\x00MTrk\x00\x00\x00(\x00\xc1\x10\x00\x917@\x10\x817\x00\x00\x917@\x10\x817\x00\x00\x91@@\x10\x81@\x00\x10\x917@\x81 \x817\x00\x00\xff/\x00"""
        s = SMF([test1, test2], instruments=[0, 16])
        s.write(out_fd, title="test song")
        actual_bytes = out_fd.getvalue()

        self.assertEqual(expected_bytes, actual_bytes)

    def test_velocity(self):
        from sebastian.midi.write_midi import Trk

        t = Trk()
        t.start_note(0, 1, 60, 10)
        self.assertEqual(b'\x00\x91\x3c\x0a', t.data.getvalue())

    def test_velocity_from_note(self):
        from sebastian.core import OSequence, Point
        from sebastian.core import OFFSET_64, MIDI_PITCH, DURATION_64

        test = OSequence([
            Point({OFFSET_64: o, MIDI_PITCH: m, DURATION_64: d}) for (o, m, d) in [
                (0, 60, 16), (16, 72, 16), (32, 64, 16)
            ]
        ])

        test[0]['velocity'] = 10
        test[1]['velocity'] = 255

        from sebastian.midi.write_midi import SMF
        from io import BytesIO
        out_fd = BytesIO(bytearray())

        expected_bytes = b'MThd\x00\x00\x00\x06\x00\x01\x00\x02\x00\x10MTrk\x00\x00\x00&\x00\xffX\x04\x04\x02\x18\x08\x00\xffY\x02\x00\x00\x00\xffQ\x03\x07\xa1 \x00\xff\x03\ttest song\x00\xff/\x00MTrk\x00\x00\x00\x1f\x00\xc0\x00\x00\x90<\x0A\x10\x80<\x00\x00\x90H\xff\x10\x80H\x00\x00\x90@@\x10\x80@\x00\x00\xff/\x00'

        s = SMF([test])
        s.write(out_fd, title="test song")
        actual_bytes = out_fd.getvalue()

        self.assertEqual(expected_bytes, actual_bytes)

    def test_velocity_from_note_with_invalid_velocities(self):
        from sebastian.core import OSequence, Point
        from sebastian.core import OFFSET_64, MIDI_PITCH, DURATION_64

        test = OSequence([
            Point({OFFSET_64: o, MIDI_PITCH: m, DURATION_64: d}) for (o, m, d) in [
                (0, 60, 16), (16, 72, 16), (32, 64, 16)
            ]
        ])

        test[0]['velocity'] = -1
        test[1]['velocity'] = 300

        from sebastian.midi.write_midi import SMF
        from io import BytesIO
        out_fd = BytesIO(bytearray())

        expected_bytes = b'MThd\x00\x00\x00\x06\x00\x01\x00\x02\x00\x10MTrk\x00\x00\x00&\x00\xffX\x04\x04\x02\x18\x08\x00\xffY\x02\x00\x00\x00\xffQ\x03\x07\xa1 \x00\xff\x03\ttest song\x00\xff/\x00MTrk\x00\x00\x00\x1f\x00\xc0\x00\x00\x90<\x00\x10\x80<\x00\x00\x90H\xff\x10\x80H\x00\x00\x90@@\x10\x80@\x00\x00\xff/\x00'

        s = SMF([test])
        s.write(out_fd, title="test song")
        actual_bytes = out_fd.getvalue()

        self.assertEqual(expected_bytes, actual_bytes)
