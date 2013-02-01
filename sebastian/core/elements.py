
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


class SeqBase:
    
    def __init__(self, *elements):
        if len(elements) == 1:
            if isinstance(elements[0], list) or isinstance(elements[0], SeqBase):
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
    
    def __eq__(self, other):
        return isinstance(other, self.__class__) and self._elements == other._elements
    
    def __ne__(self, other):
        return not (isinstance(other, self.__class__) and self._elements == other._elements)
    
    def map_points(self, func):
        return self.__class__([func(Point(point)) for point in self._elements])
        
    
    def transform(self, func):
        """
        applies function to a sequence to produce a new sequence
        """
        return func(self)
    
    __or__ = transform


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
