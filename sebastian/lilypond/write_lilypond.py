def lily_format(seq):
    return " ".join(point["lilypond"] for point in seq)


def output(seq):
    return "{ %s }" % lily_format(seq)


def write(filename, seq):
    with open(filename, "w") as f:
        f.write(output(seq))
