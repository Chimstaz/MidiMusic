"""Bass line related stuff."""
from basicNotesDefinitions import OCTAVE
import random
from collections import deque


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
                bassLine.appen(repeatnote)
                j += 1
            if pj == j:
                bassLine.append(bassLine[-1])
                j += 1
            else:
                pj = j
    return bassLine
