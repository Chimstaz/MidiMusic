"""Bass line related stuff."""
from basicNotesDefinitions import OCTAVE
from Line import Line
import random
from collections import deque
from MyUtils import coalesce
import programInstruments as pI
from itertools import chain


class BassGenerator:
    """Collect parameters and generate bass line using random values if necesery."""

    def __init__(
                self, notesPerBar=None, hoppPossibility=None,
                walkPossibility=None, repeatnotePossibility=None,
                lengthInBars=None, instrument=None,
                concatenatePossibility=None, pitch=None):
        """."""
        self.notesPerBar = notesPerBar
        self.hoppPossibility = hoppPossibility
        self.walkPossibility = walkPossibility
        self.repeatnotePossibility = repeatnotePossibility
        self.lengthInBars = lengthInBars
        self.instrument = instrument
        self.concatenatePossibility = concatenatePossibility
        self.pitch = pitch

    def Generate(self, chordLine, motiveLength=1, maxNotesPerBar=1, basePitch=60):
        """Set state of the object ."""
        glengthInBars = coalesce(self.lengthInBars, motiveLength*random.randint(1, len(chordLine)/motiveLength))
        gnotesPerBar = coalesce(self.notesPerBar, random.randint(1, maxNotesPerBar))
        ghoppPossibility = coalesce(self.hoppPossibility, random.random())
        gwalkPossibility = coalesce(self.walkPossibility, random.random())
        grepeatnotePossibility = coalesce(self.repeatnotePossibility, random.random())
        ginstrument = coalesce(self.instrument, random.choice(list(chain(pI.Bass, pI.Brass, pI.Percussive, pI.ChromaticPercussion))))
        gconcatenatePossibility = coalesce(self.concatenatePossibility, 0)
        gpitch = coalesce(self.pitch, OCTAVE*random.randint(-2, 0) + basePitch)
        gline = GenerateBass(
            chordLine=chordLine[0:glengthInBars],
            density=gnotesPerBar,
            hoppPossibility=ghoppPossibility,
            walkPossibility=gwalkPossibility,
            repeatnotePossibility=grepeatnotePossibility
            )
        return Line(glengthInBars, gnotesPerBar, ginstrument, gline, gconcatenatePossibility, gpitch)


def GenerateBass(chordLine, density, hoppPossibility=0.5, walkPossibility=0.5, repeatnotePossibility=0.5):
    """Generate bass for given chords line.

    Chord line should be list of chords where chord is list of notes.
    Density is number of bass notes between chords.
    """
    if density == 0 or chordLine == []:
        return []
    bassLine = []
    repeatnote = random.choice(random.choice(chordLine))
    if walkPossibility + hoppPossibility != 0:
        # Generate base bass
        baseLine = [random.choice(x) for x in chordLine]
    else:
        baseLine = [repeatnote] * len(chordLine)

    baseLine.append(baseLine[-1])

    hoppingpattern = deque([OCTAVE*random.choice([-1, 1]) for x in range(density * 3)])
    for i in range(len(chordLine)):
        bassLine.append(baseLine[i])
        j = 0
        pj = 0
        while j < (density-1):
            if random.random() < walkPossibility:
                if bassLine[-1] < baseLine[i]:
                    bassLine.append(random.randint(bassLine[-1], baseLine[i]))
                else:
                    bassLine.append(random.randint(baseLine[i], bassLine[-1]))
                j += 1
            if random.random() < hoppPossibility and j < density-1:
                hop = hoppingpattern.popleft()
                bassLine.append(bassLine[-1] + hop)
                hoppingpattern.append(hop)
                j += 1
            if random.random() < repeatnotePossibility and j < density-1:
                bassLine.append(repeatnote)
                j += 1
            if pj == j:
                bassLine.append(bassLine[-1])
                j += 1
            else:
                pj = j
    return bassLine
