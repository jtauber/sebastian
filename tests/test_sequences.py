from unittest import TestCase


class TestSequences(TestCase):

    def make_point(self, offset=0):
        from sebastian.core import Point
        from sebastian.core import OFFSET_64, DURATION_64, MIDI_PITCH
        retval = Point({
            OFFSET_64: 16 + offset,
            MIDI_PITCH: 50 + offset,
            DURATION_64: 17 + offset,
        })
        return retval

    def make_sequence(self, offset=0):
        points = [self.make_point(offset), self.make_point(offset + 3)]
        from sebastian.core import OSequence
        return OSequence(points)

    def test_make_sequence(self):
        """
        Ensure sequences are composed of notes in the correct order
        """
        p1 = self.make_point()
        p2 = self.make_point(offset=50)  # we need to dedupe somehow
        from sebastian.core import OSequence
        from sebastian.core import OFFSET_64, MIDI_PITCH, DURATION_64
        sequence = OSequence([p1, p2])
        self.assertEqual(sequence._elements, [
            {DURATION_64: 17, OFFSET_64: 16, MIDI_PITCH: 50},
            {DURATION_64: 17 + 50, OFFSET_64: 16 + 50, MIDI_PITCH: 50 + 50}
        ])

    def test_sequence_last_point(self):
        """
        Ensure that OSequence.last_point returns the highest offset note
        """
        points = [self.make_point(offset=x) for x in range(100, -1, -10)]
        from sebastian.core import OSequence
        from sebastian.core import OFFSET_64, MIDI_PITCH, DURATION_64
        sequence = OSequence(points)
        self.assertEqual(sequence.last_point(), {
            DURATION_64: 17 + 100, OFFSET_64: 16 + 100, MIDI_PITCH: 50 + 100
        })

    def test_sequence_last_point_empty(self):
        """
        Ensure OSequence.last_point doesn't barf when the sequence is empty
        """
        from sebastian.core import OSequence
        from sebastian.core import OFFSET_64, DURATION_64
        sequence = OSequence([])
        self.assertEqual(sequence.last_point(), {
            DURATION_64: 0, OFFSET_64: 0
        })

    def test_sequence_reflexive_concat(self):
        """
        Ensure sequences can concatenate reflexively
        """
        #from sebastian.core import OFFSET_64, DURATION_64, MIDI_PITCH
        s1 = self.make_sequence()
        concated = s1 + s1
        from sebastian.core import OFFSET_64, MIDI_PITCH, DURATION_64
        self.assertEqual(concated._elements, [
            {MIDI_PITCH: 50, OFFSET_64: 16, DURATION_64: 17},
            {MIDI_PITCH: 53, OFFSET_64: 19, DURATION_64: 20},
            {MIDI_PITCH: 50, OFFSET_64: 55, DURATION_64: 17},
            {MIDI_PITCH: 53, OFFSET_64: 58, DURATION_64: 20}
        ])

    def test_sequence_concat(self):
        """
        Ensure sequences can concatenate
        """
        s1 = self.make_sequence()
        s2 = self.make_sequence(offset=50)
        concated = s1 + s2
        from sebastian.core import OFFSET_64, MIDI_PITCH, DURATION_64
        self.assertEqual(concated._elements, [
            {MIDI_PITCH: 50, OFFSET_64: 16, DURATION_64: 17},
            {MIDI_PITCH: 53, OFFSET_64: 19, DURATION_64: 20},
            {MIDI_PITCH: 100, OFFSET_64: 105, DURATION_64: 67},
            {MIDI_PITCH: 103, OFFSET_64: 108, DURATION_64: 70}
        ])

    def test_sequence_repeats(self):
        """
        Ensure sequences can be repeated
        """
        s1 = self.make_sequence()
        repeat = s1 * 2
        from sebastian.core import OFFSET_64, MIDI_PITCH, DURATION_64
        self.assertEqual(repeat._elements, [
            {MIDI_PITCH: 50, OFFSET_64: 16, DURATION_64: 17},
            {MIDI_PITCH: 53, OFFSET_64: 19, DURATION_64: 20},
            {MIDI_PITCH: 50, OFFSET_64: 55, DURATION_64: 17},
            {MIDI_PITCH: 53, OFFSET_64: 58, DURATION_64: 20}
        ])

    def test_sequence_repeats_more(self):
        """
        Ensure MOAR repetition works
        """
        s1 = self.make_sequence()
        repeat = s1 * 3

        from sebastian.core import OFFSET_64, MIDI_PITCH, DURATION_64
        self.assertEqual(repeat._elements, [
            {MIDI_PITCH: 50, OFFSET_64: 16, DURATION_64: 17},
            {MIDI_PITCH: 53, OFFSET_64: 19, DURATION_64: 20},
            {MIDI_PITCH: 50, OFFSET_64: 55, DURATION_64: 17},
            {MIDI_PITCH: 53, OFFSET_64: 58, DURATION_64: 20},
            {MIDI_PITCH: 50, OFFSET_64: 94, DURATION_64: 17},
            {MIDI_PITCH: 53, OFFSET_64: 97, DURATION_64: 20}
        ])

    def test_sequence_merge(self):
        """
        Ensure two sequences can be merged into one sequence
        """
        s1 = self.make_sequence()
        s2 = self.make_sequence(offset=1)

        merged = s1 // s2
        from sebastian.core import OFFSET_64, MIDI_PITCH, DURATION_64
        self.assertTrue(merged._elements, [
            {MIDI_PITCH: 50, OFFSET_64: 16, DURATION_64: 17},
            {MIDI_PITCH: 51, OFFSET_64: 17, DURATION_64: 18},
            {MIDI_PITCH: 53, OFFSET_64: 19, DURATION_64: 20},
            {MIDI_PITCH: 54, OFFSET_64: 20, DURATION_64: 21}
        ])

    def test_empty_sequence_merge(self):
        """
        Ensure that an empty sequence merge is an identity operation
        """
        s1 = self.make_sequence()
        from sebastian.core import OSequence
        s2 = OSequence([])
        merged = s1 // s2
        from sebastian.core import OFFSET_64, DURATION_64, MIDI_PITCH
        self.assertEqual(merged._elements, [
            {MIDI_PITCH: 50, OFFSET_64: 16, DURATION_64: 17},
            {MIDI_PITCH: 53, OFFSET_64: 19, DURATION_64: 20}
        ])
