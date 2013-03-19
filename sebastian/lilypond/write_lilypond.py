def output(seq):
    return "{ %s }" % " ".join(point["lilypond"] for point in seq)


def write(filename, seq):
    with open(filename, "w") as f:
        f.write(output(seq))
