"""Generating whole music."""
from Chords import GenerateChordsGroupsLine, GenerateChordsLine
from Bass import BassGenerator
from Melody import MelodyGenerator
from MyUtils import coalesce
import random
from Line import addLineToTrack
from midiutil.MidiFile import MIDIFile
import programInstruments as pI
from itertools import chain


class MidiMusic:
    """Class doing all steps to get midi file with music."""

    def __init__(
            self, seed=None, motiveLength=None, musicLength=None, notesPerBar=None, tempo=None,
            numberOfBassLines=None, bassLinesOptions=None,
            numberOfMelodyLines=None, melodyLinesOptions=None,
            basePitch=None, chordInstrument=None):
        """Initialization of MidiMusic."""
        self.seed = seed
        self.motiveLength = motiveLength
        self.musicLength = musicLength
        self.bassLinesOptions = coalesce(bassLinesOptions, [])
        self.numberOfBassLines = numberOfBassLines
        self.melodyLinesOptions = coalesce(melodyLinesOptions, [])
        self.numberOfMelodyLines = numberOfMelodyLines
        self.tempo = tempo
        self.notesPerBar = notesPerBar
        self.basePitch = basePitch
        self.chordInstrument = chordInstrument

    def generate(self, output):
        """Generate music using acctual state of object."""
        # general
        random.setstate(self.randomStates[0])
        generatedNotesPerBar = coalesce(self.notesPerBar, random.randint(1, 8))
        generatedNumberOfBassLines = coalesce(self.numberOfBassLines, random.randint(0, 2))
        generatedNumberOfMelodyLines = coalesce(self.numberOfMelodyLines, random.randint(0, 2))
        generatedTempo = coalesce(self.tempo, random.randint(80, 220))
        genertedPitch = coalesce(self.basePitch, random.randint(48, 72))

        # chord line
        random.setstate(self.randomStates[1])
        chordLine = GenerateChordsLine(GenerateChordsGroupsLine(coalesce(self.motiveLength, random.randint(1, 6))))
        genertaedMotiveLength = len(chordLine)
        chordLine *= coalesce(self.musicLength, random.randint(1, 4))
        lines = []

        # bass
        random.setstate(self.randomStates[2])
        for i in range(generatedNumberOfBassLines):
            nextRandomSet = random.randint(0, len(self.randomStates)-1)
            if len(self.bassLinesOptions) > i:
                if self.bassLinesOptions[i] is None:
                    self.bassLinesOptions[i] = BassGenerator()
            else:
                self.bassLinesOptions.append(BassGenerator())
            lines.append(self.bassLinesOptions[i].generate(chordLine, genertaedMotiveLength, generatedNotesPerBar, genertedPitch))
            random.setstate(self.randomStates[nextRandomSet])

        # melody
        random.setstate(self.randomStates[3])
        for i in range(generatedNumberOfMelodyLines):
            nextRandomSet = random.randint(0, len(self.randomStates)-1)
            if len(self.melodyLinesOptions) > i:
                if self.melodyLinesOptions[i] is None:
                    self.melodyLinesOptions[i] = MelodyGenerator()
            else:
                self.melodyLinesOptions.append(MelodyGenerator())
            lines.append(self.melodyLinesOptions[i].generate(chordLine, genertaedMotiveLength, generatedNotesPerBar, genertedPitch))
            random.setstate(self.randomStates[nextRandomSet])

        # Percussion
        # MakeMidi
        random.setstate(self.randomStates[5])
        # chordLine *= coalesce(self.musicLength, random.randint(1, 4))
        genertaedMusicLength = len(chordLine)
        MyMIDI = MIDIFile(1+generatedNumberOfBassLines+generatedNumberOfMelodyLines)
        volume = 200//((2+generatedNumberOfBassLines+generatedNumberOfMelodyLines)//2)
        MyMIDI.addTrackName(0, 0, "ChordLine")
        MyMIDI.addTempo(0, 0, generatedTempo)
        MyMIDI.addProgramChange(0, 0, 0, coalesce(self.chordInstrument, random.choice(list(chain(pI.Guitar, pI.Piano)))))
        for i, chord in enumerate(chordLine):
            for x in chord:
                MyMIDI.addNote(0, 0, x+genertedPitch, i*generatedNotesPerBar+1, generatedNotesPerBar, volume)

        random.setstate(self.randomStates[6])
        for i, line in enumerate(lines):
            nextRandomSet = random.randint(0, len(self.randomStates)-1)
            addLineToTrack(MyMIDI, i+1, 0, line, genertaedMusicLength*generatedNotesPerBar, generatedNotesPerBar, volume)
            MyMIDI.addTrackName(i+1, 0, "Track"+str(i+1))
            MyMIDI.addTempo(i+1, 0, generatedTempo)
            random.setstate(self.randomStates[nextRandomSet])

        binfile = open(output, 'wb')
        MyMIDI.writeFile(binfile)
        binfile.close()

    @property
    def seed(self):
        """."""
        return self._seed

    @seed.setter
    def seed(self, seed):
        """Set new seed for random parameters."""
        self._seed = coalesce(seed, random.randint(0, 100000000))
        random.seed(self._seed)
        self.randomStates = []
        for s in random.choices(range(1, 0xFFFF), k=10):
            random.seed(s)
            self.randomStates.append(random.getstate())
