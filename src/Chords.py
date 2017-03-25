"""Chords."""
from basicNotesDefinitions import ChordType, Notes
import random


ChordGroups = [
            [[x+Notes.C for x in ChordType.Major], [x+Notes.C for x in ChordType.Major7], [x+Notes.C for x in ChordType.Major6]],
            [[x+Notes.D for x in ChordType.Minor], [x+Notes.D for x in ChordType.Minor7], [x+Notes.F for x in ChordType.Major6]],
            [[x+Notes.E for x in ChordType.Minor], [x+Notes.E for x in ChordType.Minor7], [x+Notes.E for x in ChordType.Major6]],
            [[x+Notes.F for x in ChordType.Major], [x+Notes.F for x in ChordType.Major7], [x+Notes.F for x in ChordType.Major6], [x+Notes.D for x in ChordType.Minor7]],
            [[x+Notes.G for x in ChordType.Major], [x+Notes.G for x in ChordType.Dominant7], [x+Notes.Db for x in ChordType.Dominant7]],
            [[x+Notes.A for x in ChordType.Minor], [x+Notes.A for x in ChordType.Minor7], [x+Notes.C for x in ChordType.Major6]],
            [[x+Notes.H for x in ChordType.Diminished], [x+Notes.H for x in ChordType.DiminishedHalf], [x+Notes.D for x in ChordType.Minor6]]
            ]


def GenerateChordsGroupsLine(length):
    """Generate list of groups from which choose chords."""
    ChordGroupsPath = [
        {0, 3, 4},
        {1, 3, 4, 6},
        {2, 1, 3},
        {3, 0, 4, 5, 6},
        {4, 0, 3, 5},
        {5, 1, 3, 4},
        {6, 0, 2}
        ]
    ChordLast = {0, 3, 4, 6}  # Line can end only at chods from these groups
    ChordBeforeLast = {0, 1, 3, 4, 5, 6}  # All except 2 group can reach last chord in one move
    ChordLine = [0]
    for i in range(length):
        if i == length-1:
            ChordLine.append(random.sample(ChordGroupsPath[ChordLine[-1]].intersection(ChordLast), 1)[0])
        elif i == length-2:
            ChordLine.append(random.sample(ChordGroupsPath[ChordLine[-1]].intersection(ChordBeforeLast), 1)[0])
        else:
            ChordLine.append(random.sample(ChordGroupsPath[ChordLine[-1]], 1)[0])
    return ChordLine


def GenerateChordsLine(GroupsLine):
    """Generate chords line from groups of chords."""
    ChordsLine = []
    for gr in GroupsLine:
        ChordsLine.append(random.choice(ChordGroups[gr]))
    return ChordsLine
