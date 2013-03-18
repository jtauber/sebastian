from unittest import TestCase


class TestPoint(TestCase):

    def make_point(self):
        from sebastian.core import Point
        from sebastian.core import OFFSET_64, DURATION_64, MIDI_PITCH
        retval = Point({
            OFFSET_64: 16,
            MIDI_PITCH: 50,
            DURATION_64: 17,
        })
        return retval

    def test_point_tuple(self):
        """
        Ensure Point.tuple works in the nominal case
        """
        p1 = self.make_point()
        from sebastian.core import OFFSET_64, DURATION_64
        self.assertEqual(p1.tuple(OFFSET_64, DURATION_64), (16, 17))

    def test_point_tuple_empty(self):
        """
        Ensure Point.tuple works when passed no arguments
        """
        p1 = self.make_point()
        self.assertEqual(p1.tuple(), ())

    def test_point_flags_valid(self):
        """
        Ensure that OFFSET_64, DURATION_64, and MIDI_PITCH are not equal
        """
        import sebastian.core
        self.assertNotEqual(sebastian.core.OFFSET_64, sebastian.core.DURATION_64)
        self.assertNotEqual(sebastian.core.OFFSET_64, sebastian.core.MIDI_PITCH)
        self.assertNotEqual(sebastian.core.DURATION_64, sebastian.core.MIDI_PITCH)

    def test_point_flags_hashable(self):
        """
        Ensure the constant flags are hashable - by asserting their value
        """
        from sebastian.core import OFFSET_64, DURATION_64, MIDI_PITCH
        self.assertEqual(OFFSET_64, OFFSET_64)
        self.assertEqual(DURATION_64, DURATION_64)
        self.assertEqual(MIDI_PITCH, MIDI_PITCH)
