import sys
import json
import argparse

parser = argparse.ArgumentParser()

parser.add_argument("-c", default="parallel") # parallel or serial (parallel by default, I guess)
parser.add_argument("-f")
parser.add_argument("-o")
parser.add_argument("-l")
parser.add_argument("--math-mode-delimiters", action="store_true")
parser.add_argument("--regular-text", action="store_true")
parser.add_argument('--no-frequencies', action='store_true')

args = parser.parse_args()

if args.l:
    with open(args.l) as f:
        labels = f.read().splitlines()
        label = lambda event_type: labels[event_type] if event_type < len(labels) else str(event_type)
else:
    label = lambda event_type: str(event_type)

f = sys.stdin if args.f is None else open(args.f)
out = sys.stdout if args.o is None else open(args.o, "w")

j = json.load(f)

for episode in j['episodes']:

    elements = [label(e) for e in episode['event-types']]
    frequency = episode.get('frequency')

    elements_it = ("\\text{{{}}}".format(e) for e in elements) if args.regular_text \
        else elements

    if args.c == "parallel":
        latexified = "\\{{ {} \\}}".format(", ".join(elements_it))
    else:
        latexified = " \\to ".join(elements_it)

    if args.math_mode_delimiters:
        latexified = "$ {} $".format(latexified)

    if not args.no_frequencies and frequency is not None:
        latexified = "{} ({:.3g})".format(latexified, frequency)

    print(latexified, file=out)


f.close()
out.close()
