import sys
import json
import argparse

def latexify_episode(episode, args):
    if not isinstance(episode, dict):
        return None
    if not 'event-types' in episode:
        return None

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

    return latexified

def latexify(thing, args):
    if isinstance(thing, dict) and 'event-types' in thing:
        latexified = latexify_episode(thing, args)

        return latexified if latexified is not None else None

    if isinstance(thing, dict):
        new_thing = {}
        # new_thing = {key : latexify(item, args) for key, item in thing.items()}
        for key, item in thing.items():
            new_thing[key] = latexify(item, args)
        return new_thing

    if isinstance(thing, list):
        return [latexify(item, args) for item in thing]


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

latexified = latexify(j, args)

print('Global top k:', file=out)
print('\n'.join(latexified['top-k-episodes']['global']), file=out)
print('Per-size top k:', file=out)
print('\n'.join('{}-episodes:\n{}'.format(
    i, '\n'.join(str(e) for e in i_episodes)) for i, i_episodes in enumerate(latexified['top-k-episodes']['per-size'], start=1)), file=out)
print('All episodes:', file=out)
print('\n'.join(latexified['episodes']), file=out)


f.close()
out.close()
