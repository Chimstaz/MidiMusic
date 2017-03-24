"""Generating whole music."""
from Chords import GenerateChordsGroupsLine, GenerateChordsLine
from Bass import BassLineOptions, BassSpecification
from Melody import MelodySpecification
from MyUtils import coalesce
import programInstruments
from itertools import chain
import random


class MidiMusic:
    """Class doing all steps to get midi file with music."""

    def __init__(
            self, seed=None, motiveLenght=None, musicLenght=None, notesPerBar=None, tempo=None,
            numberOfBassLines=None, bassLinesOptions=None,
            melodyOptions=None):
        """Initialization of MidiMusic."""
        self.setSeed(seed)
        self.motiveLenght = motiveLenght
        self.musicLenght = musicLenght
        self.bassLinesOptions = coalesce(bassLinesOptions, [])
        self.numberOfBassLines = numberOfBassLines
        self.melodyOptions = [melodyOptions]
        self.tempo = tempo
        self.notesPerBar = notesPerBar

    def generate(self, output):
        """Generate music using acctual state of object."""
        # chord line
        random.setstate(self.randomStates[0])
        generatedNotesPerBar = coalesce(self.notesPerBar, random.randint(1, 8))
        chordLine = GenerateChordsLine(GenerateChordsGroupsLine(coalesce(self.motiveLenght, random.randint(1, 6))))
        genertaedMotiveLenght = len(chordLine)
        chordLine *= coalesce(self.musicLenght, random.randint(1, 4))
        genertaedMusicLenght = len(chordLine)
        # bass
        generatedBassLinesOptions = self._bassLinesOptions(generatedNotesPerBar, genertaedMotiveLenght, genertaedMusicLenght)
        bassLines = []
        random.setstate(self.randomStates[1])
        for bo in generatedBassLinesOptions:
            nextRandomSet = random.randint(0, len(self.randomStates)-1)
            bassLines.append(bo.Generate(chordLine))
            random.setstate(self.randomStates[nextRandomSet])
        # self._melodyLine = self

    def _bassLinesOptions(self, notesPerBar, motiveLenght, musicLenght):
        random.setstate(self.randomStates[1])
        bassLinesOpt = []
        for x in range(0, coalesce(self.numberOfBassLines, random.randint(0, 2))):
            if len(self.bassLinesOptions) <= x or self.bassLinesOptions[x] is None:
                bassLinesOpt.append(BassLineOptions(
                                            bassOptions=BassSpecification(
                                                                        notesPerBar=random.randint(1, notesPerBar),
                                                                        hoppPossibility=random.random(),
                                                                        walkPossibility=random.random(),
                                                                        repeatnotePossibility=random.random()),
                                            lenghtInBars=random.randrange(motiveLenght, musicLenght+1, musicLenght),
                                            instrument=random.choice(chain(programInstruments.Bass, programInstruments.Brass))
                                            ))
            else:
                bassSpec = None
                if self.bassLinesOptions[x].bassOptions is None:
                    bassSpec = BassSpecification(
                                    notesPerBar=random.randint(1, notesPerBar),
                                    hoppPossibility=random.random(),
                                    walkPossibility=random.random(),
                                    repeatnotePossibility=random.random())
                else:
                    bassSpec = BassSpecification(
                                    notesPerBar=coalesce(self.bassLinesOptions[x].bassOptions.notesPerBar, random.randint(1, notesPerBar)),
                                    hoppPossibility=coalesce(self.bassLinesOptions[x].bassOptions.hoppPossibility, random.random()),
                                    walkPossibility=coalesce(self.bassLinesOptions[x].bassOptions.walkPossibility, random.random()),
                                    repeatnotePossibility=coalesce(self.bassLinesOptions[x].bassOptions.repeatnotePossibility, random.random()))
                bassLinesOpt.append(BassLineOptions(
                            bassOptions=bassSpec,
                            lenghtInBars=coalesce(self.bassLinesOptions[x].lenghtInBars, random.randrange(motiveLenght, musicLenght+1, musicLenght)),
                            instrument=coalesce(self.bassLinesOptions[x].instrument, random.choice(chain(programInstruments.Bass, programInstruments.Brass)))))
        return bassLinesOpt

    def setSeed(self, seed):
        """Set new seed for random parameters."""
        random.seed(seed)
        self.randomStates = []
        for s in random.choices(range(1, 0xFFFFFFFF), 10):
            random.seed(s)
            self.randomStates.append(random.getstate())
