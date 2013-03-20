from unittest import TestCase


class TestTransforms(TestCase):

    def make_point(self, offset=0):
        from sebastian.core import Point
        from sebastian.core import OFFSET_64, DURATION_64
        retval = Point({
            OFFSET_64: 16 + offset,
            "pitch": 50 + offset,
            DURATION_64: 17 + offset,
        })
        return retval

    def make_sequence(self, offset=0):
        points = [self.make_point(offset), self.make_point(offset + 3)]
        from sebastian.core import OSequence
        return OSequence(points)

    def test_transpose(self):
        """
        Ensure transpose modifies the pitch
        """
        from sebastian.core.transforms import transpose
        s1 = self.make_sequence()
        transposed = s1 | transpose(12)
        from sebastian.core import OFFSET_64, DURATION_64

        self.assertEqual(transposed._elements, [
            {"pitch": 62, OFFSET_64: 16, DURATION_64: 17},
            {"pitch": 65, OFFSET_64: 19, DURATION_64: 20}
        ])

    def test_transponse_reversable(self):
        """
        Ensure that transpose is reversable
        """
        from sebastian.core.transforms import transpose
        s1 = self.make_sequence()
        transposed = s1 | transpose(5) | transpose(-5)
        self.assertEqual(s1, transposed)

    def test_reverse(self):
        """
        Ensure puts points in a sequence backwards
        """
        from sebastian.core.transforms import reverse
        s1 = self.make_sequence()
        reversed = s1 | reverse()
        from sebastian.core import OFFSET_64, DURATION_64

        self.assertEqual(reversed._elements, [
            {"pitch": 53, OFFSET_64: 0, DURATION_64: 20},
            {"pitch": 50, OFFSET_64: 6, DURATION_64: 17},
            {OFFSET_64: 39}
        ])

    def test_reversed_doesnt_modify_next_offset(self):
        """
        Ensure reversed sequences are the same length as their input
        """
        from sebastian.core.transforms import reverse
        s1 = self.make_sequence()
        reversed = s1 | reverse()
        self.assertEqual(s1.next_offset(), reversed.next_offset())

    def test_reverse_is_reversable(self):
        """
        Ensure that a double reverse of a sequence is idempotent
        """
        from sebastian.core.transforms import reverse
        s1 = self.make_sequence()
        reversed = s1 | reverse() | reverse()
        self.assertEqual(s1._elements, reversed._elements)

    def test_stretch(self):
        """
        Ensure that strech modifies a simple sequence
        """
        from sebastian.core.transforms import stretch
        s1 = self.make_sequence()
        streched = s1 | stretch(2)

        from sebastian.core import OFFSET_64, DURATION_64, MIDI_PITCH
        self.assertEqual(streched._elements, [
            {"pitch": 50, OFFSET_64: 32, DURATION_64: 34},
            {"pitch": 53, OFFSET_64: 38, DURATION_64: 40}
        ])

    def test_strech_is_reversable(self):
        """
        Ensure that stretch and contract is an identity operation
        """
        from sebastian.core.transforms import stretch
        s1 = self.make_sequence()
        stretched = s1 | stretch(2) | stretch(0.5)
        self.assertEqual(s1._elements, stretched._elements)

    def test_dynamics(self):
        from sebastian.core.transforms import dynamics
        s1 = self.make_sequence()
        dynamiced = s1 | dynamics('ff')
        self.assertEqual([p.tuple('velocity') for p in dynamiced], [(94,), (94,)])

    def test_all_dynamic_markers(self):
        from sebastian.core.transforms import dynamics
        s1 = self.make_sequence()
        velocities = ['pppppp', 'ppppp', 'pppp', 'ppp', 'pp', 'p', 'mp', 'mf', 'f', 'ff', 'fff', 'ffff']
        for velocity in velocities:
            dynamiced = s1 | dynamics(velocity)
            self.assertTrue('velocity' in dynamiced[0])

    def test_dynamics_linear_crecendo(self):
        from sebastian.core.transforms import dynamics
        s1 = self.make_sequence()
        s1 = s1 * 5
        velocitied = s1 | dynamics('ppp', 'fff')
        self.assertEqual([p['velocity'] for p in velocitied], [24, 34, 44, 54, 64, 74, 84, 94, 104, 114])

    ## TODO: inversion tests don't make sense yet, since inversion
    ## will be rewritten
    # def test_invert_flips_a_sequence(self):
    #     """
    #     Ensure inverting a sequence modifies the pitch
    #     """
    #     from sebastian.core.transforms import invert
    #     s1 = self.make_sequence()
    #     inverted = s1 | invert(50)

    #     from sebastian.core import OFFSET_64, DURATION_64, MIDI_PITCH
    #     self.assertEqual(inverted._elements, [
    #         {MIDI_PITCH: 50, OFFSET_64: 16, DURATION_64: 17},
    #         {MIDI_PITCH: 47, OFFSET_64: 19, DURATION_64: 20}
    #     ])

    # def test_invert_is_reversable(self):
    #     """
    #     Ensure reversing twice generates the same sequence
    #     """
    #     from sebastian.core.transforms import invert
    #     s1 = self.make_sequence()
    #     inverted = s1 | invert(50) | invert(50)

    #     self.assertEqual(inverted._elements, s1._elements)

    def make_notes(self):
        return [1, 2, 3, 1]

    def make_horizontal_sequence(self):
        from sebastian.core import HSeq, Point
        return HSeq([Point(degree=degree) for degree in self.make_notes()])

    def test_hseq_list(self):
        """
        Ensure list of hseq returns reasonable results
        """
        h1 = self.make_horizontal_sequence()

        for point, degree in zip(list(h1), self.make_notes()):
            self.assertEqual(point, {'degree': degree})

    def test_add_transformation(self):
        """
        Ensure adding properties modifies the points
        """
        from sebastian.core.transforms import add
        h1 = self.make_horizontal_sequence()
        from sebastian.core import DURATION_64

        added = h1 | add({'octave': 4, DURATION_64: 8})

        expected = [{'degree': degree, DURATION_64: 8, 'octave': 4} for degree in self.make_notes()]

        self.assertEqual(list(added), expected)

    def test_degree_in_key(self):
        """
        Ensure that it plays in G major.
        """
        from sebastian.core.transforms import degree_in_key
        from sebastian.core.notes import Key, major_scale
        h1 = self.make_horizontal_sequence()
        keyed = h1 | degree_in_key(Key("G", major_scale))

        self.assertEqual(keyed._elements, [
            {'degree': 1, 'pitch': -1},
            {'degree': 2, 'pitch': 1},
            {'degree': 3, 'pitch': 3},
            {'degree': 1, 'pitch': -1},
        ])

    def test_degree_in_key_with_octave(self):
        """
        Ensure that degree in key with octave is sane
        """
        from sebastian.core.transforms import degree_in_key_with_octave
        from sebastian.core.notes import Key, major_scale

        h1 = self.make_horizontal_sequence()
        keyed = h1 | degree_in_key_with_octave(Key("C", major_scale), 4)

        self.assertEqual(keyed._elements, [
            {'degree': 1, 'octave': 4, 'pitch': -2},
            {'degree': 2, 'octave': 4, 'pitch': 0},
            {'degree': 3, 'octave': 4, 'pitch': 2},
            {'degree': 1, 'octave': 4, 'pitch': -2}
        ])

    def test_play_notes_in_midi_pitches(self):
        """
        Ensure that it plays in G major.
        """
        from sebastian.core.transforms import degree_in_key, midi_pitch, add
        from sebastian.core.notes import Key, major_scale
        from sebastian.core import MIDI_PITCH, DURATION_64
        h1 = self.make_horizontal_sequence()
        keyed = h1 | degree_in_key(Key("G", major_scale))
        positioned = keyed | add({'octave': 4, DURATION_64: 8})
        pitched = positioned | midi_pitch()

        self.assertEqual(pitched._elements, [
            {'degree': 1, 'pitch': -1, DURATION_64: 8, MIDI_PITCH: 55, 'octave': 4},
            {'degree': 2, 'pitch': 1, DURATION_64: 8, MIDI_PITCH: 57, 'octave': 4},
            {'degree': 3, 'pitch': 3, DURATION_64: 8, MIDI_PITCH: 59, 'octave': 4},
            {'degree': 1, 'pitch': -1, DURATION_64: 8, MIDI_PITCH: 55, 'octave': 4},
        ])

    def test_lilypond_transform(self):
        """
        Ensure that it plays in G major.
        """
        from sebastian.core.transforms import midi_pitch, add, lilypond
        from sebastian.core import DURATION_64
        from sebastian.core import HSeq, Point
        h1 = HSeq([Point(pitch=pitch) for pitch in [0, 1, 2, 3, 4, 11, -4, -11]])
        positioned = h1 | add({'octave': 4, DURATION_64: 8})
        pitched = positioned | midi_pitch()
        pitched[3]['octave'] = 5
        pitched[4]['octave'] = 3
        lilyed = pitched | lilypond()

        import pprint
        pprint.pprint(list(lilyed))

        self.assertEqual(lilyed._elements, [
            {'duration_64': 8,
              'lilypond': 'd8',
              'midi_pitch': 50,
              'octave': 4,
              'pitch': 0},
             {'duration_64': 8,
              'lilypond': 'a8',
              'midi_pitch': 57,
              'octave': 4,
              'pitch': 1},
             {'duration_64': 8,
              'lilypond': 'e8',
              'midi_pitch': 52,
              'octave': 4,
              'pitch': 2},
             {'duration_64': 8,
              'lilypond': "b'8",
              'midi_pitch': 59,
              'octave': 5,
              'pitch': 3},
             {'duration_64': 8,
              'lilypond': 'fis,8',
              'midi_pitch': 54,
              'octave': 3,
              'pitch': 4},
             {'duration_64': 8,
              'lilypond': 'fisis8',
              'midi_pitch': 55,
              'octave': 4,
              'pitch': 11},
             {'duration_64': 8,
              'lilypond': 'b8',
              'midi_pitch': 58,
              'octave': 4,
              'pitch': -4},
             {'duration_64': 8,
              'lilypond': 'b8',
              'midi_pitch': 57,
              'octave': 4,
              'pitch': -11}
        ])


    def test_lilypond_transform_rhythms(self):
        """
        Ensure points without pitches can render to lilypond
        """
        from sebastian.core.transforms import midi_pitch, add, lilypond
        from sebastian.core import DURATION_64
        from sebastian.core import HSeq, Point
        h1 = HSeq([
            Point({DURATION_64: 64}),
            Point({DURATION_64: 0}),
            Point()
        ])
        h2 = h1 | lilypond()
        self.assertEqual(h2._elements[0]['lilypond'], r"\xNote c'1")
        self.assertEqual(h2._elements[1]['lilypond'], '')
        self.assertEqual(h2._elements[2]['lilypond'], '')

    def test_subseq(self):
        from sebastian.core.transforms import subseq
        from sebastian.core import OSeq, Point
        OffsetSequence = OSeq("offset", "duration")

        s1 = OffsetSequence(
            Point(a=2, offset=0),
            Point(a=2, offset=20),
            Point(a=2, offset=25),
            Point(a=2, offset=30),
            Point(a=2, offset=50),
        )
        s2 = s1 | subseq(20, 30)
        self.assertEqual(
            s2,
            OffsetSequence(
                Point(a=2, offset=20),
                Point(a=2, offset=25)
            )
        )
