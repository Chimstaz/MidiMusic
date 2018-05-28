"""Common for bass and melody lines."""
from collections import namedtuple
import random


Line = namedtuple("Line", "lengthInBars, notesPerBar, instrument, line, concatenatePossibility, pitchModifier")


def addLineToTrack(MIDIObject, track, channel, lineDesc, endTime, barTime, volume):
    """Add notes to track in MIDIObject."""
    MIDIObject.addProgramChange(track, channel, 0, lineDesc.instrument)
    concat = [(lineDesc.line[0], 1)]
    for i in range(1, len(lineDesc.line)):
        if concat[-1][0] == lineDesc.line[i] and random.random() < lineDesc.concatenatePossibility:
            p = concat.pop()
            concat.append((p[0], p[1]+1))
        else:
            concat.append((lineDesc.line[i], 1))
    time = 0
    unitTime = barTime/lineDesc.notesPerBar
    while True:
        for i, n in enumerate(concat):
            MIDIObject.addNote(track, channel, lineDesc.pitchModifier+n[0], time+1, n[1]*unitTime, volume)
            time += n[1]*unitTime
            if time >= endTime:
                return
