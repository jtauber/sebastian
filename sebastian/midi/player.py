## The goal of this module is to eventually be to MIDI players what
## 'webbrowser' is to Web browsers.
##
## Personally, I only need it to work on OS X so patches accepted for other
## operating systems.

import sys
import tempfile
import subprocess

from sebastian.midi import write_midi

def play(sequence):
    if sys.platform == "darwin":
        
        f = tempfile.NamedTemporaryFile(suffix=".mid", delete=False)
        s = write_midi.SMF(sequence)
        s.write(f)
        f.close()
        
        subprocess.call(["open", f.name])
    else:
        print "Only OS X supported at the moment. Patches accepted!"
