#!/usr/bin/env python

"""
A library for parsing Standard MIDI Files (SMFs).

Currently it just outputs the data it finds.
"""


class Base:
    """
    Base is a generic base class for parsing binary files. It cannot be
    instantiated directly, you need to sub-class it and implement a parse()
    method.
    
    Your sub-class can then be instantiated with a single argument, a byte
    array.
    
    Base provides a number of basic methods for pulling data out of the byte
    array and incrementing the index appropriately.
    """
    
    def __init__(self, data):
        self.data = data
        self.index = 0
        self.parse()
    
    def peek_byte(self):
        data = self.data[self.index]
        return ord(data)
    
    def get_byte(self):
        data = self.data[self.index]
        self.index += 1
        return ord(data)
    
    def get_char(self, length=1):
        data = self.data[self.index:self.index + length]
        self.index += length
        return data
    
    def get_ushort(self):
        data = 0
        data += self.get_byte() << 8
        data += self.get_byte() << 0
        return data
    
    def get_ulong(self):
        data = 0
        data += self.get_byte() << 24
        data += self.get_byte() << 16
        data += self.get_byte() << 8
        data += self.get_byte() << 0
        return data
    
    def get_varlen(self):
        data = 0
        while True:
            next = self.get_byte()
            high_bit = next // 0x80
            data = (data << 7) + (next % 0x80)
            if not high_bit:
                return data


class SMF(Base):
    """
    A parser for Simple MIDI files.
    """
    
    def parse_chunk(self):
        chunk_id = self.get_char(4)
        length = self.get_ulong()
        data = self.get_char(length)
        return chunk_id, data
    
    def parse(self):
        while self.index < len(self.data):
            chunk_id, data = self.parse_chunk()
            if chunk_id == "MThd":
                Thd(data)
            elif chunk_id == "MTrk":
                Trk(data)
            else:
                print chunk_id
                pass  # ignore unknown chunk type


class Thd(Base):
    """
    A parser for the Thd chunk in a MIDI file.
    """
    
    def parse(self):
        format = self.get_ushort()
        num_tracks = self.get_ushort()
        division = self.get_ushort()
        print "Thd", format, num_tracks, division


class Trk(Base):
    """
    A parser for the Trk chunk in a MIDI file.
    """
    
    def process_event(self, time_delta, status):
        if status == 0xFF:
            status2 = self.get_byte()
            varlen2 = self.get_varlen()
            data = self.get_char(varlen2)
            if status2 == 0x03:
                print "sequence/track name '%s'" % data
            elif status2 == 0x04:
                print "instrument '%s'" % data
            elif status2 == 0x2F:
                assert varlen2 == 0, varlen2
                self.track_end = True
                print "track end"
            elif status2 == 0x51:
                assert varlen2 == 3, varlen2
                print "tempo %d %d %d" % (ord(data[0]), ord(data[1]), ord(data[2]))
            elif status2 == 0x54:
                assert varlen2 == 5, varlen2
                print "smpte %d %d %d %d %d" % (ord(data[0]), ord(data[1]), ord(data[2]), ord(data[3]), ord(data[4]))
            elif status2 == 0x58:
                assert varlen2 == 4, varlen2
                print "time signature %d %d %d %d" % (ord(data[0]), ord(data[1]), ord(data[2]), ord(data[3]))
            elif status2 == 0x59:
                assert varlen2 == 2, varlen2
                print "key signature %d %d" % (ord(data[0]), ord(data[1]))  # @@@ first arg signed?
            else:
                raise Exception("unknown metaevent status " + hex(status2))
        elif 0x80 <= status <= 0xEF:
            event_type, channel = divmod(status, 0x10)
            if event_type == 0x8:  # note off
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
            elif event_type == 0x9:  # note on
                note_number = self.get_byte()
                velocity = self.get_byte()
                self.ticks += time_delta
                self.current_note = (channel + 1, note_number, self.ticks)
                # print "event", "%s:%s:%s" % (bar + 1, beat, tick), time_delta, "note_on", channel + 1, note_number, velocity
            elif event_type == 0xB:  # controller
                controller = self.get_byte()
                value = self.get_byte()
                print "event", time_delta, "controller", channel + 1, controller, value
            elif event_type == 0xC:  # program change
                program = self.get_byte()
                print "event", time_delta, "program", channel + 1, program
            else:
                raise Exception("unknown event type " + hex(event_type))
        else:
            raise Exception("unknown status " + hex(status))
    
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
            else:  # running status
                self.process_event(time_delta, status)  # previous status
        if not self.track_end:
            raise Exception("no track end")


if __name__ == "__main__":
    track = -1
    import sys
    filename = sys.argv[1]
    f = SMF(open(filename).read())
