

def write(filename, seq):
    with open(filename, "w") as f:
        f.write("{ ")
        for point in seq:
            f.write(point["lilypond"])
            f.write(" ")
        f.write("}\n")


if __name__ == "__main__":
    from sebastian.core import DURATION_64
    from sebastian.core import HSeq, Point
    from sebastian.core.notes import Key, major_scale
    from sebastian.core.transforms import degree_in_key, add, lilypond

    seq = HSeq(Point(degree=n) for n in [1, 2, 3, 4])
    seq = seq | add({DURATION_64: 16, "octave": 5})

    C_major = Key("C", major_scale)

    seq = seq | degree_in_key(C_major) | lilypond()

    write("test.ly", seq)
