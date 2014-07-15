from collections import Iterable
import tempfile
import subprocess as sp

try:
    from IPython.core.display import Image, SVG
    ipython = True
except ImportError:
    ipython = False

from sebastian.lilypond import write_lilypond


class UnificationError(Exception):
    pass


class Point(dict):

    def unify(self, other):
        new = self.copy()
        for key, value in other.items():
            if key in new:
                if new[key] != value:
                    raise UnificationError(key)
            else:
                new[key] = value
        return Point(new)

    def tuple(self, *attributes):
        return tuple(self.get(attribute) for attribute in attributes)

    __mod__ = unify


class SeqBase(object):

    def __init__(self, *elements):
        if len(elements) == 1:
            if isinstance(elements[0], Point):
                elements = [elements[0]]
            elif isinstance(elements[0], Iterable):
                elements = list(elements[0])
        else:
            elements = list(elements)
        self._elements = []

        for point in elements:
            self.append(point)

    def __getitem__(self, item):
        return self._elements[item]

    def __len__(self):
        return len(self._elements)

    def __iter__(self):
        return iter(self._elements)

    def __eq__(self, other):
        return isinstance(other, self.__class__) and self._elements == other._elements

    def __ne__(self, other):
        return not (isinstance(other, self.__class__) and self._elements == other._elements)

    def map_points(self, func):
        return self.__class__([func(point=Point(point)) for point in self._elements])

    def transform(self, func):
        """
        applies function to a sequence to produce a new sequence
        """
        return func(self)

    def zip(self, other):
        """
        zips two sequences unifying the corresponding points.
        """
        return self.__class__(p1 % p2 for p1, p2 in zip(self, other))

    __or__ = transform
    __and__ = zip

    def display(self, format="png"):
        """
        Return an object that can be used to display this sequence.
        This is used for IPython Notebook.

        :param format: "png" or "svg"
        """
        from sebastian.core.transforms import lilypond
        seq = HSeq(self) | lilypond()

        lily_output = write_lilypond.lily_format(seq)
        if not lily_output.strip():
            #In the case of empty lily outputs, return self to get a textual display
            return self

        if format == "png":
            suffix = ".preview.png"
            args = ["lilypond", "--png", "-dno-print-pages", "-dpreview"]
        elif format == "svg":
            suffix = ".preview.svg"
            args = ["lilypond", "-dbackend=svg", "-dno-print-pages", "-dpreview"]

        f = tempfile.NamedTemporaryFile(suffix=suffix)
        basename = f.name[:-len(suffix)]
        args.extend(["-o"+basename, "-"])

        #Pass shell=True so that if your $PATH contains ~ it will
        #get expanded. This also changes the way the arguments get
        #passed in. To work correctly, pass them as a string
        p = sp.Popen(" ".join(args), stdin=sp.PIPE, shell=True)
        stdout, stderr = p.communicate("{ %s }" % lily_output)
        if p.returncode != 0:
            # there was an error
            #raise IOError("Lilypond execution failed: %s%s" % (stdout, stderr))
            return None

        if not ipython:
            return f.read()
        if format == "png":
            return Image(data=f.read(), filename=f.name, format="png")
        else:
            return SVG(data=f.read(), filename=f.name)

    def __repr__(self):
        return "%s(%r)" % (self.__class__.__name__, self._elements)

    def _repr_png_(self):
        f = self.display("png")
        if not isinstance(f, basestring):
            return f.data
        return f

    def _repr_svg_(self):
        f = self.display("svg")
        if not isinstance(f, basestring):
            return f.data
        return f

def OSeq(offset_attr, duration_attr):

    class _OSeq(SeqBase):

        def last_point(self):
            if len(self._elements) == 0:
                return Point({offset_attr: 0, duration_attr: 0})
            else:
                return sorted(self._elements, key=lambda x: x[offset_attr])[-1]

        def next_offset(self):
            point = self.last_point()
            return point[offset_attr] + point.get(duration_attr, 0)

        def append(self, point):
            """
            appends a copy of the given point to this sequence, calculating
            the next offset to use for it if it doesn't have one
            """
            point = Point(point)
            if offset_attr not in point:
                point[offset_attr] = self.next_offset()
            self._elements.append(point)

        def concatenate(self, next_seq):
            """
            concatenates two sequences to produce a new sequence
            """
            offset = self.next_offset()

            new_seq = _OSeq(self._elements)
            for point in next_seq._elements:
                new_point = Point(point)
                new_point[offset_attr] = new_point[offset_attr] + offset
                new_seq._elements.append(new_point)
            return new_seq

        def repeat(self, count):
            """
            repeat sequence given number of times to produce a new sequence
            """
            x = _OSeq()
            for i in range(count):
                x = x.concatenate(self)
            return x

        def merge(self, parallel_seq):
            """
            combine the points in two sequences, putting them in offset order
            """
            return _OSeq(sorted(self._elements + parallel_seq._elements, key=lambda x: x.get(offset_attr, 0)))

        def subseq(self, start_offset=0, end_offset=None):
            """
            Return a subset of the sequence
            starting at start_offset (defaulting to the beginning)
            ending at end_offset (None representing the end, whih is the default)
            """
            def subseq_iter(start_offset, end_offset):
                for point in self._elements:
                    #Skip until start
                    if point[offset_attr] < start_offset:
                        continue

                    #Yield points start_offset <=  point < end_offset
                    if end_offset is None or point[offset_attr] < end_offset:
                        yield point
                    else:
                        raise StopIteration
            return _OSeq(subseq_iter(start_offset, end_offset))

        __add__ = concatenate
        __mul__ = repeat
        __floordiv__ = merge

    return _OSeq


class HSeq(SeqBase):
    """
    a horizontal sequence where each element follows the previous
    """

    def append(self, point):
        """
        appends a copy of the given point to this sequence
        """
        point = Point(point)
        self._elements.append(point)

    def concatenate(self, next_seq):
        """
        concatenates two sequences to produce a new sequence
        """
        return HSeq(self._elements + next_seq._elements)

    def repeat(self, count):
        """
        repeat sequence given number of times to produce a new sequence
        """
        x = HSeq()
        for i in range(count):
            x = x.concatenate(self)
        return x

    def subseq(self, start_offset=0, end_offset=None):
        """
        Return a subset of the sequence
        starting at start_offset (defaulting to the beginning)
        ending at end_offset (None representing the end, whih is the default)
        Raises ValueError if duration_64 is missing on any element
        """
        from sebastian.core import DURATION_64

        def subseq_iter(start_offset, end_offset):
            cur_offset = 0
            for point in self._elements:
                try:
                    cur_offset += point[DURATION_64]
                except KeyError:
                    raise ValueError("HSeq.subseq requires all points to have a %s attribute" % DURATION_64)
                #Skip until start
                if cur_offset < start_offset:
                    continue

                #Yield points start_offset <=  point < end_offset
                if end_offset is None or cur_offset < end_offset:
                    yield point
                else:
                    raise StopIteration
        return HSeq(subseq_iter(start_offset, end_offset))

    __add__ = concatenate
    __mul__ = repeat


class VSeq(SeqBase):
    """
    a vertical sequence where each element is coincident with the others
    """

    def append(self, point):
        """
        appends a copy of the given point to this sequence
        """
        point = Point(point)
        self._elements.append(point)

    def merge(self, parallel_seq):
        """
        combine the points in two sequences
        """
        return VSeq(self._elements + parallel_seq._elements)

    __floordiv__ = merge
