#!/usr/bin/env python

from cStringIO import StringIO


def write_chars(out, chars):
    out.write(chars)


def write_byte(out, b):
    out.write(chr(b))


def write_ushort(out, s):
    write_byte(out, (s >> 8) % 256)
    write_byte(out, (s >> 0) % 256)


def write_ulong(out, l):
    write_byte(out, (l >> 24) % 256)
    write_byte(out, (l >> 16) % 256)
    write_byte(out, (l >> 8) % 256)
    write_byte(out, (l >> 0) % 256)


def write_varlen(out, n):
    data = chr(n & 0x7F)
    while True:
        n = n >> 7
        if n:
            data = chr((n & 0x7F) | 0x80) + data
        else:
            break
    out.write(data)


class SMF:
    
    def __init__(self, events):
        self.events = events
        
    def write(self, out):
        
        Thd(format=1, num_tracks=2, division=16).write(out)
        T = 1 # how to translate events times into time_delta using the division above
        
        t = Trk()
        t.sequence_track_name("untitled")
        t.time_signature(4, 2, 24, 8)
        t.key_signature(254, 0)
        t.tempo(6, 138, 27)
        t.track_end()
        t.write(out)
        
        t = Trk()
        tick = 0
        for offset, note_value, duration in self.events:
            t.start_note((offset * T) - tick, note_value)
            t.end_note(duration * T, note_value)
            tick = (offset + duration) * T
        t.track_end()
        t.write(out)


class Thd:
    
    def __init__(self, format, num_tracks, division):
        self.format = format
        self.num_tracks = num_tracks
        self.division = division
        
    def write(self, out):
        write_chars(out, "MThd")
        write_ulong(out, 6)
        write_ushort(out, self.format)
        write_ushort(out, self.num_tracks)
        write_ushort(out, self.division)


class Trk:
    
    def __init__(self):
        self.data = StringIO()
    
    def sequence_track_name(self, name):
        write_varlen(self.data, 0) # tick
        write_byte(self.data, 0xFF)
        write_byte(self.data, 0x03)
        write_varlen(self.data, len(name))
        write_chars(self.data, name)
    
    def time_signature(self, a, b, c, d):
        write_varlen(self.data, 0) # tick
        write_byte(self.data, 0xFF)
        write_byte(self.data, 0x58)
        write_varlen(self.data, 4)
        write_byte(self.data, a)
        write_byte(self.data, b)
        write_byte(self.data, c)
        write_byte(self.data, d)
    
    def key_signature(self, a, b):
        write_varlen(self.data, 0) # tick
        write_byte(self.data, 0xFF)
        write_byte(self.data, 0x59)
        write_varlen(self.data, 2)
        write_byte(self.data, a)
        write_byte(self.data, b)
    
    def tempo(self, a, b, c):
        write_varlen(self.data, 0) # tick
        write_byte(self.data, 0xFF)
        write_byte(self.data, 0x51)
        write_varlen(self.data, 3)
        write_byte(self.data, a)
        write_byte(self.data, b)
        write_byte(self.data, c)
    
    def start_note(self, time_delta, note_number):
        write_varlen(self.data, time_delta)
        write_byte(self.data, 0x91)
        write_byte(self.data, note_number)
        write_byte(self.data, 64) # velocity
    
    def end_note(self, time_delta, note_number):
        write_varlen(self.data, time_delta)
        write_byte(self.data, 0x81)
        write_byte(self.data, note_number)
        write_byte(self.data, 0) # velocity
    
    def track_end(self):
        write_varlen(self.data, 0) # tick
        write_byte(self.data, 0xFF)
        write_byte(self.data, 0x2F)
        write_varlen(self.data, 0)
    
    def write(self, out):
        write_chars(out, "MTrk")
        d = self.data.getvalue()
        write_ulong(out, len(d))
        out.write(d)


f = open("test.mid", "w")

test = [ # this is the same format as the test answers in lilypond/tests.py
(0, 60, 16), (16, 72, 16), (32, 64, 16), (48, 55, 16), (64, 74, 16), (80, 62, 16), (96, 50, 16),
(112, 48, 16), (128, 36, 16), (144, 24, 16), (160, 40, 16), (176, 55, 16), (192, 26, 16), (208, 38, 16),
(224, 50, 16), (240, 48, 16)
]

s = SMF(test)
s.write(f)
f.close()