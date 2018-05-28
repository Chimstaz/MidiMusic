"""Chords types."""
from enum import Enum, IntEnum, auto


OCTAVE = 12


class ChordType(Enum):
    """Enum with basic chord types. Notation is interval from first sound."""

    '''To generate chord add key to every element'''
    Major = [0, 4, 7]
    Major6 = [0, 4, 7, 9]
    Major7 = [0, 4, 7, 11]
    Minor = [0, 3, 7]
    Minor6 = [0, 3, 7, 9]
    Minor7 = [0, 3, 7, 10]
    Dominant7 = [0, 4, 7, 10]
    Diminished = [0, 3, 6]
    Diminished7 = [0, 3, 6, 9]
    DiminishedHalf = [0, 3, 6, 10]

    def __init__(self, notelist):
        """."""
        self.notes = notelist

    def __iter__(self):
        """Iterator on ChordType acctualy is iterator of its notes list."""
        return self.notes.__iter__()


class Notes(IntEnum):
    """Notes."""

    C = 0
    Cis = 1
    Db = 1
    D = 2
    Dis = 3
    Eb = 3
    E = 4
    F = 5
    Fis = 6
    Gb = 6
    G = 7
    Gis = 8
    Ab = 8
    A = 9
    Ais = 10
    B = 10
    Hb = 10
    H = 11
    His = 12


class Signs(Enum):
    """Special signs in lines."""

    SILENCE = auto()
    CONTINUE = auto()


MajorKeyNotes = [Notes.C, Notes.D, Notes.E, Notes.F, Notes.G, Notes.A, Notes.H]
MinorKeyNotes = [Notes.C, Notes.D, Notes.Eb, Notes.F, Notes.G, Notes.Ab, Notes.B]
