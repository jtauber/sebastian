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

    def test_point_tuple_arbitrary_data(self):
        """
        Ensure points can handle arbitrary data
        """
        from sebastian.core import Point
        p1 = Point(a=1, b="foo")

        self.assertEqual(p1.tuple("b", "a"), ("foo", 1))

    def test_point_equality(self):
        """
        Ensure equals works on points
        """
        from sebastian.core import Point
        p1 = Point(a=1, b="foo")
        p2 = Point(a=1, b="foo")

        self.assertEqual(p1, p2)

    def test_point_inequality(self):
        """
        Ensure not equals works on points
        """
        from sebastian.core import Point
        p1 = Point(a=1, b="foo")
        p2 = Point(a=1, b="foo", c=3)

        self.assertNotEqual(p1, p2)

    def test_point_unification(self):
        """
        Ensure point unification works happy path
        """
        from sebastian.core import Point
        p1 = Point(a=1, b="foo")
        p2 = Point(c=3)

        unified = p1 % p2
        self.assertEqual(Point(a=1, b="foo", c=3), unified)

    def test_unification_error(self):
        """
        Ensure invalid unifications make an error
        """
        from sebastian.core import Point
        from sebastian.core.elements import UnificationError
        p1 = Point(a=1, b="foo")
        p2 = Point(a=2, b="foo")
        try:
            p1 % p2
            self.assertTrue(False)
        except UnificationError:
            self.assertTrue(True)

    def test_reflexive_unification(self):
        """
        Ensure reflexive unification is a noop
        """
        from sebastian.core import Point
        p1 = Point(a=1, b="foo")
        p2 = Point(a=1, b="foo")
        unified = p1 % p2

        self.assertEqual(p1, unified)

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
