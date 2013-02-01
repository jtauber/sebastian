#!/usr/bin/env python

from sebastian.core.elements import Point, HSeq, OSeq, VSeq, UnificationError

p1 = Point(a=1, b="foo")

assert p1.tuple("b", "a") == ("foo", 1)

p2 = Point(a=1, b="foo")

assert p1 == p2

p3 = Point(c=2)

assert p1 != p3

p4 = p1 % p3

assert p4 == Point(a=1, b="foo", c=2)

assert p1 % p2 == p1

p5 = Point(a=2)

try:
    p1 % p5
    assert False
except UnificationError:
    assert True

OffsetSequence = OSeq("offset", "duration")

s1 = OffsetSequence()
s2 = OffsetSequence([p1, p4])
s3 = OffsetSequence(p1, p4)
s4 = OffsetSequence(p1) + OffsetSequence(p4)

assert s4 == s3

s5 = OffsetSequence(Point(duration=10), Point(duration=10))

assert s5._elements[1]["offset"] == 10

s6 = OffsetSequence(p1) * 5

assert len(s6._elements) == 5
assert s6._elements[-1]["offset"] == 0

s7 = s5 * 2

assert len(s7._elements) == 4
assert s7._elements[-1]["offset"] == 30

s8 = OffsetSequence(Point(a=1, offset=0), Point(a=2, offset=20)) // OffsetSequence(Point(a=3, offset=10))

assert s8._elements[1]["a"] == 3

s9 = HSeq(p1, p3)
assert len(s9) == 2
assert s9[1] == p3


def double_a(point):
    if "a" in point:
        point["a"] *= 2
    return point

s10 = s9.map_points(double_a)
assert s10[0]["a"] == 2


def reverse(seq):
    return seq.__class__(seq._elements[::-1])

s11 = s9.transform(reverse)

assert s11[0] == p3

s12 = HSeq(p2, p4)

assert s9 + s12 == HSeq(p1, p3, p2, p4)

assert s9 * 3 == s9 + s9 + s9

s13 = VSeq(p1)

s13.append(p3)

assert s13[1] == p3

assert s13 == VSeq(p1) // VSeq(p3)

assert HSeq(p1, p3) != VSeq(p1, p3)
assert not (HSeq(p1, p3) == VSeq(p1, p3))
