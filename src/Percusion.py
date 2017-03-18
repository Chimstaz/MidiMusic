"""Enumerator with all percussion sounds."""
from enum import IntEnum


PercussionChannel = 9


class Percussion(IntEnum):
    """Enum with all typical instruments in midi."""

    BassDrum2 = 34
    BassDrum1 = 35
    SideStickRimshot = 36
    SnareDrum1_AcousticSnare = 37
    HandClap = 38
    SnareDrum2_ElectricSnare = 39
    LowTom2 = 40
    ClosedHi_hat = 41
    LowTom1 = 42
    PedalHi_hat = 43
    MidTom2 = 44
    OpenHi_hat = 45
    MidTom1 = 46
    HighTom2 = 47
    CrashCymbal1 = 48
    HighTom1 = 49
    RideCymbal1 = 50
    ChineseCymbal = 51
    RideBell = 52
    Tambourine = 53
    SplashCymbal = 54
    Cowbell = 55
    CrashCymbal2 = 56
    VibraSlap = 57
    RideCymbal2 = 58
    HighBongo = 59
    LowBongo = 60
    MuteHighConga = 61
    OpenHighConga = 62
    LowConga = 63
    HighTimbale = 64
    LowTimbale = 65
    HighAgogo = 66
    LowAgogo = 67
    Cabasa = 68
    Maracas = 69
    ShortWhistle = 70
    LongWhistle = 71
    ShortGuiro = 72
    LongGuiro = 73
    Claves = 74
    HighWoodBlock = 75
    LowWoodBlock = 76
    MuteCuica = 77
    OpenCuica = 78
    MuteTriangle = 79
    OpenTriangle = 80
