"""M."""
# import argparse
from MidiMusic import MidiMusic
from ArgumentParser import ParseArgs
from programInstruments import Instrument
from Bass import BassGenerator
from Melody import MelodyGenerator

args = ParseArgs()

if args.instrumentList:
    print("Instruments list: ")
    for i in Instrument:
        print(i.name)
    exit()

bassOpt = []
for b in args.basslines:
    bassOpt.append(BassGenerator(
                        notesPerBar=b.notesPerBar,
                        hoppPossibility=b.hopp,
                        walkPossibility=b.walk,
                        repeatnotePossibility=b.repeat,
                        lengthInBars=b.length,
                        instrument=b.instrument,
                        concatenatePossibility=b.concat,
                        pitch=b.pitch
                        ))

melodyOpt = []
for m in args.melodylines:
    melodyOpt.append(MelodyGenerator(
                        notesPerBar=m.notesPerBar,
                        jumpPossibility=m.jump,
                        lengthInBars=m.length,
                        instrument=m.instrument,
                        concatenatePossibility=m.concat,
                        pitch=m.pitch,
                        key=[n for nl in m.key for n in nl]
                        ))

mm = MidiMusic(
    seed=args.seed,
    musicLength=args.musicLength,
    motiveLength=args.ml,
    notesPerBar=args.notesPerBar,
    tempo=args.tempo,
    basePitch=args.pitch,
    numberOfBassLines=args.nb,
    bassLinesOptions=bassOpt,
    numberOfMelodyLines=args.nm,
    melodyLinesOptions=melodyOpt,
    chordInstrument=args.chordInstrument
    )
mm.generate(args.output)
print("Used seed: " + str(mm.seed))
