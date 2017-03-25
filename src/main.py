"""M."""
# import argparse
from MidiMusic import MidiMusic
from ArgumentParser import ParseArgs

ParseArgs()
# import sys
# from io import TextIOWrapper, BytesIO
#
#
# parser = argparse.ArgumentParser()
# parserin = argparse.ArgumentParser(prog="-t", add_help=False)
# parserin.add_argument("-u", "--uhu", type=int, action="append")
# parserin.add_argument("--rest", nargs="*", action="append")
#
#
# parser.add_argument("-s", "--seed", type=int, help="Seed of the random")
# parser.add_argument("-b", "--bassLines", type=int, help="How many bass lines to generate")
# parser.add_argument("-t", "--test", action="append", metavar="")
#
# # hack to get default usage and modify it
# # parser has only print_usage, so I have to read it from redirected stdout
# # setup the environment
# old_stdout = sys.stdout
# sys.stdout = TextIOWrapper(BytesIO(), sys.stdout.encoding)
#
# # do something that writes to stdout or stdout.buffer
# parser.print_usage()
#
# # get output
# pos = sys.stdout.tell()
# sys.stdout.seek(0)       # jump to the start
# defusage = sys.stdout.readline()  # read output
#
# sys.stdout.seek(pos)
# parserin.print_usage()
#
# # get output
# pos2 = sys.stdout.tell()
# sys.stdout.seek(pos+7)       # jump to the start
# tpos = defusage.find("-t")
# inusage = sys.stdout.readline()[:-1]
# inusage = inusage[:3] + "\"" + inusage[3:-1] + "\""
# defusage = defusage[:tpos] + inusage + defusage[tpos+2:]  # read output
#
#
# # restore stdout
# sys.stdout.close()
# sys.stdout = old_stdout
#
# print(defusage)
#
# args = parser.parse_args(None)
# argsin = parserin.parse_args([y for x in range(len(args.test)) for y in args.test[x].split(" ")])
# print(args)
# print(argsin)
#
# parserin.print_help()
#

mm = MidiMusic(numberOfBassLines=3, numberOfMelodyLines=3)
mm.generate("output.mid")

# cl = Chords.GenerateChordsGroupsLine(3)
# print(cl)
# cl = Chords.GenerateChordsLine(cl)
# print(cl)
#
# per = random.sample(list(Percussion), 5)
# pl = []
# for x in range(len(cl)*4):
#     pl.append([])
#     for i in range(random.randrange(0, 5)):
#         if random.random() < 0.4:
#             pl[x].append(random.choice(per))
# pl = pl * 8
#
# cl = cl * 2
# bl = Bass.GenerateBass(cl, 4, walkPossibility=0, repeatnotePossibility=0, hoppPossibility=1)
# ml = Melody.GenerateMelody(cl, 4, MajorKeyNotes)
# cl = cl * 4
# bl = bl * 4
# ml = ml * 4
#
# # Create the MIDIFile Object with 1 track
# MyMIDI = MIDIFile(4)
#
# # Tracks are numbered from zero. Times are measured in beats.
# trackc = 0
# trackb = 1
# trackm = 2
# trackp = 3
# time = 0
#
# # Add track name and tempo.
# MyMIDI.addTrackName(trackc, time, "ChordLine")
# MyMIDI.addTempo(trackc, time, 180)
#
# MyMIDI.addTrackName(trackb, time, "BassLine")
# MyMIDI.addTempo(trackb, time, 180)
#
# MyMIDI.addTrackName(trackm, time, "MelodyLine2")
# MyMIDI.addTempo(trackm, time, 180)
#
# MyMIDI.addTrackName(trackp, time, "PercussionLine2")
# MyMIDI.addTempo(trackp, time, 180)
#
# # Add a note. addNote expects the following information:
# channel = 0
# pitch = 60
# time = 0
# duration = 4
# chordlen = 4
# volume = 100
#
# # Now add the note.
# for i in range(len(cl)):
#     for x in cl[i]:
#         MyMIDI.addNote(trackc, channel, pitch+x, (time+i)*chordlen, chordlen, volume)
#
# for i in range(len(pl)):
#     for x in pl[i]:
#         MyMIDI.addNote(trackp, PercussionChannel, x, time+i, 1, volume)
#
# for i in range(len(bl)):
#     MyMIDI.addNote(trackb, channel, pitch-24+bl[i], (time+i)*chordlen/4, 1, volume)
#
# # for i in range(len(ml)):
# #    MyMIDI.addNote(trackm, channel, pitch+ml[i], (time+i)*chordlen/4, 4/4, volume)
#
# compresm = [(ml[0], 1)]
# for i in range(1, len(ml)):
#     if compresm[-1][0] == ml[i]:
#         p = compresm.pop()
#         compresm.append((p[0], p[1]+1))
#     else:
#         compresm.append((ml[i], 1))
# for i in range(len(compresm)):
#     MyMIDI.addNote(trackm, channel, pitch+compresm[i][0], time, compresm[i][1], volume)
#     time += compresm[i][1]
#
# # MyMIDI.addNote(track, channel, pitch, time, duration, volume)
# # MyMIDI.addNote(track, channel, pitch+1, time+1, duration, volume)
# # MyMIDI.addNote(track, channel, pitch+3, time+3, duration, volume)
# # MyMIDI.addNote(track, channel, pitch+2, time+2, duration, volume)
# MyMIDI.addProgramChange(trackc, channel, time, Instrument.AcousticGuitar_nylon)
# MyMIDI.addProgramChange(trackb, channel, time, Instrument.ElectricBass_finger)
# MyMIDI.addProgramChange(trackm, channel, time, Instrument.AcousticGrandPiano)
#
#
# # And write it to disk.
# binfile = open("output.mid", 'wb')
# MyMIDI.writeFile(binfile)
# binfile.close()

# # Instantiate the class with a tempo (120bpm is the default) and an output file destination.
# mymidi = MIDITime(120, 'myfile.mid')

# # Create a list of notes. Each note is a list: [time, pitch, velocity,duration]
# midinotes = [
#     [0, 60, 127, 4],  # At 0 beats (the start), Middle C with velocity 127, for 3 beats
#     [2, 55, 127, 6],
#     [2, 50, 127, 6],
#     [2, 45, 127, 6],
#     [2, 40, 127, 6],
#     [10, 61, 127, 4]  # At 10 beats (12 seconds from start), C#5 with velocity 127, for 4 beats
# ]

# # Add a track with those notes
# mymidi.add_track(midinotes)

# # Output the .mid file
# mymidi.save_midi()
