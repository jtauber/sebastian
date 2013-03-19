from unittest import TestCase

from sebastian.midi.midi import load_midi


class TestMidi(TestCase):

    def test_load_midi(self):
        import os.path
        filename = os.path.join(os.path.dirname(__file__), "scale.mid")
        self.assertEqual(
            list(load_midi(filename)[0]),
            [
                {'midi_pitch': 60, 'offset_64': 42, 'duration_64': 15},
                {'midi_pitch': 62, 'offset_64': 56, 'duration_64': 7},
                {'midi_pitch': 64, 'offset_64': 63, 'duration_64': 6},
                {'midi_pitch': 65, 'offset_64': 70, 'duration_64': 6},
                {'midi_pitch': 67, 'offset_64': 77, 'duration_64': 5},
                {'midi_pitch': 69, 'offset_64': 84, 'duration_64': 5},
                {'midi_pitch': 71, 'offset_64': 91, 'duration_64': 6},
                {'midi_pitch': 72, 'offset_64': 98, 'duration_64': 14},
                {'midi_pitch': 71, 'offset_64': 113, 'duration_64': 6},
                {'midi_pitch': 69, 'offset_64': 120, 'duration_64': 7},
                {'midi_pitch': 67, 'offset_64': 127, 'duration_64': 6},
                {'midi_pitch': 65, 'offset_64': 134, 'duration_64': 5},
                {'midi_pitch': 64, 'offset_64': 141, 'duration_64': 4},
                {'midi_pitch': 62, 'offset_64': 147, 'duration_64': 4},
                {'midi_pitch': 60, 'offset_64': 154, 'duration_64': 13},
            ]
        )
