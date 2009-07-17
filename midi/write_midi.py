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
    
    def write(self, out):
        
        Thd(format=1, num_tracks=1, division=120).write(out)
        t = Trk()
        t.sequence_track_name("untitled")
        t.time_signature(4, 2, 24, 8)
        t.key_signature(254, 0)
        t.tempo(6, 138, 27)
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


class xxTrk:
    
    def process_event(self, time_delta, status):
        if 0x80 <= status <= 0xEF:
            event_type = status // 0x10
            channel = status % 0x10
            if event_type == 0x8: # note off
                note_number = self.get_byte()
                velocity = self.get_byte()
                self.ticks += time_delta
                if self.current_note[0] == channel + 1 and self.current_note[1] == note_number:
                    pass
                else:
                    raise Exception("overlapping notes")
                start_ticks = self.current_note[2]
                beat, tick = divmod(start_ticks, 480)
                bar, beat = divmod(beat, 4)
                est_dur = divmod(time_delta + 21, 60)
                assert est_dur[1] == 0
                est_dur = est_dur[0]
                tick = divmod(tick, 60)
                assert tick[1] == 0
                tick = tick[0]
                note_name = divmod(note_number, 12)
                if self.next_note != start_ticks:
                    rest = divmod(start_ticks - self.next_note, 60)
                    assert rest[1] == 0
                    rest = rest[0]
                    print "0:0:%d" % rest,
                if bar + 1 > self.prev_bar:
                    print "\n# bar %s" % (bar + 1)
                    self.prev_bar = bar + 1
                print "%d:%d:%d" % (note_name[0], note_name[1], est_dur),
                self.next_note = start_ticks + (est_dur * 60)
            elif event_type == 0x9: # note on
                note_number = self.get_byte()
                velocity = self.get_byte()
                self.ticks += time_delta
                self.current_note = (channel + 1, note_number, self.ticks)
                # print "event", "%s:%s:%s" % (bar + 1, beat, tick), time_delta, "note_on", channel + 1, note_number, velocity
            elif event_type == 0xB: # controller
                controller = self.get_byte()
                value = self.get_byte()
                pass #print "event", time_delta, "controller", channel + 1, controller, value
            elif event_type == 0xC: # program change
                program = self.get_byte()
                pass #print "event", time_delta, "program", channel + 1, program
            else:
                raise Exception("unknown event type " + hex(event_type))
    
    def parse(self):
        self.ticks = 0
        self.next_note = 0
        self.prev_bar = 0
        global track
        track += 1
        print "\n## Track %s" % track
        self.track_end = False
        while self.index < len(self.data):
            if self.track_end:
                raise Exception("more data after track end")
            time_delta = self.get_varlen()
            next_byte = self.peek_byte()
            if next_byte >= 0x80:
                status = self.get_byte()
                self.process_event(time_delta, status)
            else: # running status
                self.process_event(time_delta, status) # previous status
        if not self.track_end:
            raise Exception("no track end")

f = open("test.mid", "w")
s = SMF()
s.write(f)
f.close()