#!/usr/bin/env python

"""
A library for parsing Standard MIDI Files (SMFs).

Currently it just outputs the data it finds.
"""

from sebastian.core import OSequence, Point, OFFSET_64, MIDI_PITCH, DURATION_64


class Base(object):
    """
    Base is a generic base class for parsing binary files. It cannot be
    instantiated directly, you need to sub-class it and implement a parse()
    method.
    
    Your sub-class can then be instantiated with a single argument, a byte
    array.
    
    Base provides a number of basic methods for pulling data out of the byte
    array and incrementing the index appropriately.
    """
    
    def __init__(self, data, handler):
        self.data = data
        self.handler = handler
        self.index = 0
        self.init()
        self.parse()
    
    def init(self):
        pass

    def peek_byte(self):
        return self.data[self.index]
    
    def get_byte(self):
        data = self.data[self.index]
        self.index += 1
        return data
    
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
                Thd(data, self.handler)
            elif chunk_id == "MTrk":
                Trk(data, self.handler)
            else:
                raise Exception("unknown chunk type")


class Thd(Base):
    """
    A parser for the Thd chunk in a MIDI file.
    """
    
    def parse(self):
        format = self.get_ushort()
        num_tracks = self.get_ushort()
        division = self.get_ushort()
        self.handler.header(format, num_tracks, division)


class Trk(Base):
    """
    A parser for the Trk chunk in a MIDI file.
    """
    
    def init(self):
        self.note_started = {}

    def process_event(self, time_delta, status):
        if status == 0xFF:
            status2 = self.get_byte()
            varlen2 = self.get_varlen()
            data = self.get_char(varlen2)
            if status2 == 0x01:
                self.handler.text_event(data)
            elif status2 == 0x03:
                self.handler.track_name(data)
            elif status2 == 0x04:
                self.handler.instrument(data)
            elif status2 == 0x2F:
                assert varlen2 == 0, varlen2
                self.track_end = True
                self.handler.track_end()
            elif status2 == 0x51:
                assert varlen2 == 3, varlen2
                self.handler.tempo(data[0], data[1], data[2])
            elif status2 == 0x54:
                assert varlen2 == 5, varlen2
                self.handler.smpte(data[0], data[1], data[2], data[3], data[4])
            elif status2 == 0x58:
                assert varlen2 == 4, varlen2
                self.handler.time_signature(data[0], data[1], data[2], data[3])
            elif status2 == 0x59:
                assert varlen2 == 2, varlen2
                self.handler.key_signature(data[0], data[1])  # @@@ first arg signed?
            else:
                raise Exception("unknown metaevent status " + hex(status2))
        elif 0x80 <= status <= 0xEF:
            event_type, channel = divmod(status, 0x10)
            if event_type == 0x8:  # note off
                note_number = self.get_byte()
                velocity = self.get_byte()
                self.ticks += time_delta
                if note_number not in self.note_started:
                    # note was never started so ignore
                    pass
                else:
                    start_ticks, start_velocity = self.note_started.pop(note_number)
                    duration = self.ticks - start_ticks
                self.handler.note(start_ticks, channel + 1, note_number, duration)
            elif event_type == 0x9:  # note on
                note_number = self.get_byte()
                velocity = self.get_byte()
                self.ticks += time_delta
                
                if velocity > 0:
                    if note_number in self.note_started:
                        # new note at that pitch started before previous finished
                        # not sure it should happen but let's handle it anyway
                        start_ticks, start_velocity = self.note_started.pop(note_number)
                        duration = self.ticks - start_ticks
                        self.handler.note(start_ticks, channel + 1, note_number, duration)
                    self.note_started[note_number] = self.ticks, velocity
                else:  # note end
                    if note_number not in self.note_started:
                        # note was never started so ignore
                        pass
                    else:
                        start_ticks, start_velocity = self.note_started.pop(note_number)
                        duration = self.ticks - start_ticks
                    self.handler.note(start_ticks, channel + 1, note_number, duration)

                self.current_note = (channel + 1, note_number, self.ticks)
            elif event_type == 0xB:  # controller
                controller = self.get_byte()
                value = self.get_byte()
                self.handler.controller(time_delta, channel + 1, controller, value)
            elif event_type == 0xC:  # program change
                program = self.get_byte()
                self.handler.program_change(time_delta, channel + 1, program)
            else:
                raise Exception("unknown event type " + hex(event_type))
        else:
            raise Exception("unknown status " + hex(status))
    
    def parse(self):
        self.ticks = 0
        self.next_note = 0
        global track
        track += 1
        self.handler.track_start(track)
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


class BaseHandler(object):
    
    def header(self, format, num_tracks, division):
        pass

    def text_event(self, text):
        pass

    def track_name(self, name):
        pass

    def instrument(self, name):
        pass

    def track_start(self, track_num):
        pass

    def track_end(self):
        pass

    def tempo(self, t1, t2, t3):
        pass

    def smpte(self, s1, s2, s3, s4, s5):
        pass

    def time_signature(self, t1, t2, t3, t4):
        pass

    def key_signature(self, k1, k2):
        pass

    def controller(self, time_delta, channel, controller, value):
        pass

    def program_change(self, time_delta, channel, program):
        pass

    def note(self, offset, channel, midi_pitch, duration):
        pass


class PrintHandler(BaseHandler):
    
    def header(self, format, num_tracks, division):
        print("Thd %d %d %d" % (format, num_tracks, division))

    def text_event(self, text):
        print("text event '%s'" % text)

    def track_name(self, name):
        print("sequence/track name '%s'" % name)

    def instrument(self, name):
        print("instrument '%s'" % name)

    def track_start(self, track_num):
        print("track start %d" % track_num)

    def track_end(self):
        print("track end")

    def tempo(self, t1, t2, t3):
        print("tempo %d %d %d" % (t1, t2, t3))

    def smpte(self, s1, s2, s3, s4, s5):
        print("smpte %d %d %d %d %d" % (s1, s2, s3, s4, s5))

    def time_signature(self, t1, t2, t3, t4):
        print("time signature %d %d %d %d" % (t1, t2, t3, t4))

    def key_signature(self, k1, k2):
        print("key signature %d %d" % (k1, k2))  # @@@ first arg signed?

    def controller(self, time_delta, channel, controller, value):
        print("controller %d %d %d %d" % (time_delta, channel, controller, value))

    def program_change(self, time_delta, channel, program):
        print("program change %d %d %d" % (time_delta, channel, program))

    def note(self, offset, channel, midi_pitch, duration):
        print("note %d %d %d %d" % (offset, channel, midi_pitch, duration))


class SebastianHandler(BaseHandler):

    def header(self, format, num_tracks, division):
        self.division = division
        self.tracks = [None] * num_tracks

    def track_start(self, track_num):
        self.current_sequence = OSequence()
        self.tracks[track_num] = self.current_sequence

    def note(self, offset, channel, midi_pitch, duration):
        offset_64 = 16 * offset / self.division
        duration_64 = 16 * duration / self.division
        point = Point({OFFSET_64: offset_64, MIDI_PITCH: midi_pitch, DURATION_64: duration_64})
        self.current_sequence.append(point)


def load_midi(filename):
    global track
    track = -1
    handler = SebastianHandler()
    SMF(bytearray(open(filename).read()), handler)
    return handler.tracks


if __name__ == "__main__":
    track = -1
    import sys
    filename = sys.argv[1]
    handler = SebastianHandler()
    SMF(bytearray(open(filename).read()), handler)
