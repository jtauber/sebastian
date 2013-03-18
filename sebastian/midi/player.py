## The goal of this module is to eventually be to MIDI players what
## 'webbrowser' is to Web browsers.
##
## Personally, I only need it to work on OS X so patches accepted for other
## operating systems.

import sys
import tempfile
import subprocess

from sebastian.midi import write_midi


def play(tracks):
    f = tempfile.NamedTemporaryFile(suffix=".mid", delete=False)
    s = write_midi.SMF(tracks)
    s.write(f)
    f.close()
    if sys.platform == "darwin":
        subprocess.call(["open", f.name])
    elif sys.platform == "linux2":
        subprocess.call(["timidity", f.name])
    else:
        print "Only OS X supported at the moment. Patches accepted!"
