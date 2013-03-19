from unittest import TestCase


class TestNotes(TestCase):

    def test_natural_values(self):
        from sebastian.core.notes import natural
        assert natural(-3)
        assert natural(2)
        assert natural(0)
        assert not natural(-4)
        assert not natural(5)

    def test_single_sharp(self):
        from sebastian.core.notes import single_sharp
        assert not single_sharp(0)
        assert not single_sharp(-5)
        assert single_sharp(4)
        assert not single_sharp(12)

    def test_modifiers(self):
        from sebastian.core.notes import modifiers
        assert modifiers(0) == 0
        assert modifiers(2) == 0
        assert modifiers(-1) == 0
        assert modifiers(-5) == -1
        assert modifiers(-11) == -2
        assert modifiers(-17) == -2
        assert modifiers(4) == 1
        assert modifiers(13) == 2
        assert modifiers(17) == 2

    def test_note_value(self):
        from sebastian.core.notes import value
        assert value("G#") == 6

    def test_note_names(self):
        from sebastian.core.notes import major_scale, value, name
        gsharp_major_names = [name(x) for x in major_scale(value("G#"))]
        assert gsharp_major_names == ['G#', 'A#', 'B#', 'C#', 'D#', 'E#', 'Fx']
