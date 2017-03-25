"""Stuff connected with parsing command line."""
import argparse
import sys
from io import TextIOWrapper, BytesIO
import programInstruments as pI
from basicNotesDefinitions import MajorKeyNotes, MinorKeyNotes, Notes


def _unsignedint(string):
    value = int(string)
    if value < 0:
        msg = "%r is not positive" % string
        raise argparse.ArgumentTypeError(msg)
    return value


def _possibility(string):
    value = float(string)
    if value < 0 or value > 1:
        msg = "%r is not in range [0;1]" % string
        raise argparse.ArgumentTypeError(msg)
    return value


def _instrument(string):
    try:
        value = pI.Instrument[string]
        return value
    except KeyError:
        msg = "%r is not an instrument" % string
        raise argparse.ArgumentTypeError(msg)


def _key(string):
    n = string.capitalize()
    if n == "Major":
        return MajorKeyNotes
    if n == "Minor":
        return MinorKeyNotes
    try:
        value = Notes[n]
    except KeyError:
        msg = "%r is not a note" % n
        raise argparse.ArgumentTypeError(msg)
    return [value]


def _addUsageOfLineParser(mainParser, lineParser, lineOpt):
    # hack to get default usage and modify it
    # parser has only print_usage, so I have to read it from redirected stdout
    # setup the environment
    old_stdout = sys.stdout
    sys.stdout = TextIOWrapper(BytesIO(), sys.stdout.encoding)

    mainParser.print_usage()

    # get output
    pos = sys.stdout.tell()
    sys.stdout.seek(len("usage: "))       # jump to the start
    defusage = sys.stdout.read()[:-1]  # read output, get rid of newline

    sys.stdout.seek(pos)
    lineParser.print_usage()

    sys.stdout.seek(pos+len("usage: "+lineOpt+" "))       # jump to the start of interesting part
    lineusage = sys.stdout.read()[:-1]

    # restore stdout
    sys.stdout.close()
    sys.stdout = old_stdout

    lineusage = "\n        [" + lineOpt + " \"" + lineusage + "\" ["+lineOpt+" \"...\" ...]]"

    linepos = defusage.find("["+lineOpt+"]")
    defusage = defusage[:linepos-1] + defusage[linepos+len(lineOpt)+2:] + lineusage

    mainParser.usage = defusage


def _addQuoteAtTheEndOfUsage(parser):
    # hack to get default usage and modify it
    # parser has only print_usage, so I have to read it from redirected stdout
    # setup the environment
    old_stdout = sys.stdout
    sys.stdout = TextIOWrapper(BytesIO(), sys.stdout.encoding)

    parser.print_usage()

    # get output
    sys.stdout.seek(len("usage: "))       # jump to the start
    defusage = sys.stdout.read()[:-1]  # read output, get rid of newline

    sys.stdout.close()
    sys.stdout = old_stdout

    parser.usage = defusage+"\""


def _getParserHelp(parser):
    old_stdout = sys.stdout
    sys.stdout = TextIOWrapper(BytesIO(), sys.stdout.encoding)

    parser.print_help()

    # get output
    sys.stdout.seek(0)       # jump to the start
    helpmsg = sys.stdout.read()  # read output

    sys.stdout.close()
    sys.stdout = old_stdout
    return helpmsg


def ParseArgs(ArgsList=None):
    """Parse command line arguments."""
    bassShort = "-b"
    melodyShort = "-m"

    mainParser = argparse.ArgumentParser(formatter_class=argparse.RawDescriptionHelpFormatter)

    mainParser.add_argument("-s", "--seed", type=int, help="Seed of the random")
    mainParser.add_argument("--nb", "--bassLines", type=_unsignedint, help="How many bass lines to generate", metavar="BASSLINES")
    mainParser.add_argument("--nm", "--melodyLines", type=_unsignedint, help="How many melody lines to generate", metavar="MELODYLINES")
    mainParser.add_argument("--ml", "--motiveLength", type=_unsignedint, help="Number of chords in motive", metavar="MOTIVELENGTH")
    mainParser.add_argument("-l", "--musicLength", type=_unsignedint, help="Number of times to repeat motive")
    mainParser.add_argument("-n", "--notesPerBar", type=_unsignedint, help="Maximum number of notes in bar")
    mainParser.add_argument("-t", "--tempo", type=_unsignedint, help="Tempo of music in bps")
    mainParser.add_argument("-p", "--pitch", type=_unsignedint, help="Base pitch of notes. Standard C is 60. 1 is one half tone and 12 is octave")
    mainParser.add_argument("--instrumentList", action="store_true", help="Print instrument list")

    mainParser.add_argument(bassShort, "--bass", action="append", metavar="\"BASSLINEOPTIONS\"", default=[])
    mainParser.add_argument(melodyShort, "--melody", action="append", metavar="\"MELODYLINEOPTIONS\"", default=[])

    bassParser = argparse.ArgumentParser(add_help=False, prog=bassShort+" \"", description="Bass options have to be inside qutoes. Multiple bass lines can be specifed by additional -b \"BASSLINEOPTIONS\"")
    bassgroup = bassParser.add_argument_group("bass line options")
    bassgroup.add_argument("-n", "--notesPerBar", type=_unsignedint, help="Maximum number of notes in bar in bass line")
    bassgroup.add_argument("-h", "--hopp", type=_possibility, help="Possibility of hopp in bass line (jump up or down by octave)")
    bassgroup.add_argument("-w", "--walk", type=_possibility, help="Possibility of walk pattern in bass line")
    bassgroup.add_argument("-r", "--repeat", type=_possibility, help="Possibility of repeat note in bass line")
    bassgroup.add_argument("-c", "--concat", type=_possibility, help="Possibility of concatenation equals notes into one with longer duration")
    bassgroup.add_argument("-p", "--pitch", type=_unsignedint, help="Base pitch of notes in bass line")
    bassgroup.add_argument("-l", "--length", type=_unsignedint, help="Lenght of bass line in bars. If shorter then musicLength than line will be repeated")
    bassgroup.add_argument("-i", "--instrument", type=_instrument, help="Instrument for bass line. To see instrument list use --instrumentList")

    melodyParser = argparse.ArgumentParser(add_help=False, prog=melodyShort+" \"", description="Melody options have to be inside qutoes. Multiple melody lines can be specifed by additional -m \"MELODYLINEOPTIONS\"")
    melodygroup = melodyParser.add_argument_group("melody line options")
    melodygroup.add_argument("-n", "--notesPerBar", type=_unsignedint, help="Maximum number of notes in bar in melody line")
    melodygroup.add_argument("-j", "--jump", type=_possibility, help="Possibility of jump in melody line (jump up or down by 6 half tones)")
    melodygroup.add_argument("-k", "--key", nargs="*", type=_key, help="Key of melody line. Only notes from key will be used. Could be minor, major or list of notes (eg C Dis Gb)")
    melodygroup.add_argument("-c", "--concat", type=_possibility, help="Possibility of concatenation equals notes into one with longer duration")
    melodygroup.add_argument("-p", "--pitch", type=_unsignedint, help="Base pitch of notes in melody line")
    melodygroup.add_argument("-l", "--length", type=_unsignedint, help="Lenght of melody line in bars. If shorter then musicLength than line will be repeated")
    melodygroup.add_argument("-i", "--instrument", type=_instrument, help="Instrument for melody line. To see instrument list use --instrumentList")

    _addQuoteAtTheEndOfUsage(bassParser)
    _addQuoteAtTheEndOfUsage(melodyParser)
    # _addUsageOfLineParser(mainParser, bassParser, bassShort)
    # _addUsageOfLineParser(mainParser, melodyParser, melodyShort)

    mainParser.epilog = _getParserHelp(bassParser)
    mainParser.epilog += "\n"+_getParserHelp(melodyParser)

    # mainParser.print_help()

    args = mainParser.parse_args(ArgsList)
    args.basslines = [bassParser.parse_args(b.split()) for b in args.bass]
    args.melodylines = [melodyParser.parse_args(m.split()) for m in args.melody]
    return args
    # mainParser.print_usage()
