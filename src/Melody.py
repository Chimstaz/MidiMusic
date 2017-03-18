"""Melody line related stuff."""
import random
from basicNotesDefinitions import OCTAVE, MajorKeyNotes


def GenerateMelody(chordLine, density, key=MajorKeyNotes, jumpPossibility=0.3):
    """Generate melody for given chords line.

    Chord line should be list of chords where chord is list of notes.
    Density is number of melody notes between chords.
    Key should be minor or major from basicNotesDefinitions.
    """
    keySet = [x-OCTAVE for x in key] + key + [x+OCTAVE for x in key]
    # melodyBase = [random.choice(x) for x in chordLine]
    melodyBase = [x[0] for x in chordLine]
    melodyBase.append(melodyBase[-1])
    melodyLine = []
    for i in range(len(melodyBase)-1):
        melodyLine.append(melodyBase[i])
        for j in range(density-1):
            note = 0
            if i < len(chordLine)-1:  # there is no chord to jump to in last bar
                try:
                    inKeySet = keySet.index(melodyLine[-1])
                    longjumpPossibility = [x for x in chordLine[i+1] if abs(keySet.index(x) - inKeySet) in range(5, 7)]
                except ValueError:  # note from melodyLine wasn't in key set (possible when copied from chord)
                    longjumpPossibility = []
            if len(longjumpPossibility) > 0 and random.random() < jumpPossibility:
                while j < density-2:  # put all remaining notes. Will be combine in single one leater
                    melodyLine.append(melodyLine[-1])
                    j += 1
                note = random.choice(longjumpPossibility)
                if note > melodyLine[-1]:
                    note = keySet[inKeySet+6]
                else:
                    note = keySet[inKeySet-6]
                melodyLine.append(note)
                break
            elif melodyLine[-1] < melodyBase[i+1]:
                note = random.choice([x for x in keySet if melodyLine[-1] <= x <= melodyBase[i+1]+2])
            else:
                note = random.choice([x for x in keySet if melodyBase[i+1]-2 <= x <= melodyLine[-1]])
            melodyLine.append(note)
    return melodyLine
