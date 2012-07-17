#!/usr/bin/env python

from cStringIO import StringIO

from sebastian.core import OSequence, Point, OFFSET_64, MIDI_PITCH, DURATION_64


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
    
    def __init__(self, tracks):
        self.tracks = tracks
        
    def write(self, out):
        
        num_tracks = 1 + len(self.tracks)
        Thd(format=1, num_tracks=num_tracks, division=16).write(out)
        T = 1  # how to translate events times into time_delta using the
               # division above
        
        # first track will just contain time/key/tempo info
        t = Trk()
        
        t.sequence_track_name("untitled")
        t.time_signature(4, 2, 24, 8)  # 4 4 (2nd arg is power of 2)
        t.key_signature(0, 0)  # C
        t.tempo(500000)  # in microseconds per quarter note
        t.track_end()
        t.write(out)
        
        for track in self.tracks:
            t = Trk()
            
            # we make a list of events including note off events so we can sort by
            # offset including them (to avoid negative time deltas)
            # @@@ this may eventually be a feature of sequences rather than this
            # MIDI library
            
            events_with_noteoff = []
            for point in track:
                offset, note_value, duration = point.tuple(OFFSET_64, MIDI_PITCH, DURATION_64)
                if note_value is not None:
                    events_with_noteoff.append((True, offset, note_value))
                    events_with_noteoff.append((False, offset + duration, note_value))
            
            prev_offset = None
            for on, offset, note_value in sorted(events_with_noteoff, key=lambda x: x[1]):
                if prev_offset is None:
                    time_delta = 0
                else:
                    time_delta = (offset - prev_offset) * T
                if on:
                    t.start_note(time_delta, note_value)
                else:
                    t.end_note(time_delta, note_value)
                prev_offset = offset
                
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
        write_varlen(self.data, 0)  # tick
        write_byte(self.data, 0xFF)
        write_byte(self.data, 0x03)
        write_varlen(self.data, len(name))
        write_chars(self.data, name)
    
    def time_signature(self, a, b, c, d):
        write_varlen(self.data, 0)  # tick
        write_byte(self.data, 0xFF)
        write_byte(self.data, 0x58)
        write_varlen(self.data, 4)
        write_byte(self.data, a)
        write_byte(self.data, b)
        write_byte(self.data, c)
        write_byte(self.data, d)
    
    def key_signature(self, a, b):
        write_varlen(self.data, 0)  # tick
        write_byte(self.data, 0xFF)
        write_byte(self.data, 0x59)
        write_varlen(self.data, 2)
        write_byte(self.data, a)
        write_byte(self.data, b)
    
    def tempo(self, t):
        write_varlen(self.data, 0)  # tick
        write_byte(self.data, 0xFF)
        write_byte(self.data, 0x51)
        write_varlen(self.data, 3)
        write_byte(self.data, (t >> 16) % 256)
        write_byte(self.data, (t >> 8) % 256)
        write_byte(self.data, (t >> 0) % 256)
    
    def start_note(self, time_delta, note_number):
        write_varlen(self.data, time_delta)
        write_byte(self.data, 0x91)
        write_byte(self.data, note_number)
        write_byte(self.data, 64)  # velocity
    
    def end_note(self, time_delta, note_number):
        write_varlen(self.data, time_delta)
        write_byte(self.data, 0x81)
        write_byte(self.data, note_number)
        write_byte(self.data, 0)  # velocity
    
    def track_end(self):
        write_varlen(self.data, 0)  # tick
        write_byte(self.data, 0xFF)
        write_byte(self.data, 0x2F)
        write_varlen(self.data, 0)
    
    def write(self, out):
        write_chars(out, "MTrk")
        d = self.data.getvalue()
        write_ulong(out, len(d))
        out.write(d)


if __name__ == "__main__":
    
    f = open("test.mid", "w")
    
    test = OSequence([
        Point({OFFSET_64: o, MIDI_PITCH: m, DURATION_64: d}) for (o, m, d) in [
            (0, 60, 16), (16, 72, 16), (32, 64, 16), (48, 55, 16),
            (64, 74, 16), (80, 62, 16), (96, 50, 16), (112, 48, 16),
            (128, 36, 16), (144, 24, 16), (160, 40, 16), (176, 55, 16),
            (192, 26, 16), (208, 38, 16), (224, 50, 16), (240, 48, 16)
        ]
    ])
    
    s = SMF(test)
    s.write(f)
    f.close()
