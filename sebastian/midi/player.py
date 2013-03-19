## The goal of this module is to eventually be to MIDI players what
## 'webbrowser' is to Web browsers.

import sys
import tempfile
import subprocess

from sebastian.midi import write_midi

OPEN = "open"
TIMIDITY = "timidity"


def play(tracks, program=""):
    f = tempfile.NamedTemporaryFile(suffix=".mid", delete=False)
    s = write_midi.SMF(tracks)
    s.write(f)
    f.close()
    if not program:
        if sys.platform == "darwin":
            program = OPEN
        elif sys.platform == "linux2":
            program = TIMIDITY
    if program:
        subprocess.call([program, f.name])
    else:
        print("A suitable program for your platform is unknown")
