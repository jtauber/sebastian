#!/usr/bin/env python

from sebastian.core.elements import Point, OSeq, UnificationError

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
