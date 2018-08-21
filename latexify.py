import sys
import json
import argparse

def latexify_episode(episode, args, measures=['frequency'], **kwargs):
    if not isinstance(episode, dict):
        return None
    if not 'event-types' in episode:
        return None

    elements = [label(e) for e in episode['event-types']]
    values = filter(lambda value: value is not None, (episode.get(measure) for measure in measures))

    elements_it = ("\\text{{{}}}".format(e) for e in elements) if args.regular_text \
        else elements

    if args.c == "parallel":
        latexified = "\\{{ {} \\}}".format(",\\allowbreak ".join(elements_it))
    else:
        latexified = " \\to ".join(elements_it)

    if not kwargs.get('no_math_mode_delimiters'):
        latexified = "$ {} $".format(latexified)

    if not args.no_frequencies and len(measures) > 0:
        latexified = "{} ({})".format(
            latexified, ', '.join(
                '{:.3g}'.format(value) if value != int(value) else '{}'.format(int(value)) for value in values))

    return latexified

def latexify_rule(rule, args):
    if not isinstance(rule, dict) or not 'antecedent' in rule:
        return None

    latexified = '{} \\Rightarrow {}'.format(
        latexify_episode(rule['antecedent'], args, [], no_math_mode_delimiters=True),
        latexify_episode(rule['consequent'], args, [], no_math_mode_delimiters=True))

    latexified = '$ {} $'.format(latexified)

    if 'confidence' in rule:
        confidence = rule['confidence']
        latexified = '{} ({})'.format(latexified,
            '{:.3g}'.format(confidence) if confidence != int(confidence) else '{}'.format(int(confidence)))

    return latexified

def latexify(thing, args):
    if (args.fci or args.qcsp) and hasattr(thing, 'read'):
        lines = thing.read().splitlines()
        latexifieds = []
        for line in lines:
            split = line.split()
            if args.fci:
                pattern = [item.replace('_', '\\_') for item in split[:-1]]
                (frequency, length, cohesion) = map(float, split[-1].split(';')[1:-1])
                latexifieds.append(
                    latexify_episode({'event-types': pattern, 'cohesion': cohesion},
                        args, ['cohesion']))
            else:
                pattern = split[0][1:-1].replace('_', '\\_').replace(':', '').split(',')
                cohesion = float(split[-2].replace(',', '.'))
                support = float(split[-1])

                latexifieds.append(
                    latexify_episode({'event-types': pattern, 'cohesion': cohesion, 'support': int(support)},
                        args, ['cohesion', 'support']))

        return latexifieds

    if isinstance(thing, list):
        return [latexify(item, args) for item in thing]

    if isinstance(thing, dict) and 'antecedent' in thing:
        return latexify_rule(thing, args)

    if isinstance(thing, dict) and 'event-types' in thing:
        return latexify_episode(thing, args)

    if isinstance(thing, dict):
        return  {key : latexify(item, args) for key, item in thing.items()}


parser = argparse.ArgumentParser()

parser.add_argument("-c", default="parallel") # parallel or serial (parallel by default, I guess)
parser.add_argument("-f")
parser.add_argument("-o")
parser.add_argument("-l")
parser.add_argument("--regular-text", action="store_true")
parser.add_argument('--no-frequencies', action='store_true')
parser.add_argument('--fci', action='store_true')
parser.add_argument('--qcsp', action='store_true')

args = parser.parse_args()

if args.l:
    with open(args.l) as f:
        labels = f.read().splitlines()
        label = lambda event_type: labels[event_type] if event_type < len(labels) else str(event_type)
else:
    label = lambda event_type: str(event_type)

f = sys.stdin if args.f is None else open(args.f)
out = sys.stdout if args.o is None else open(args.o, "w")

if args.fci or args.qcsp:
    latexified = list(latexify(f, args))
    for e in latexified:
        print(str(e), file=out)

else:
    j = json.load(f)
    latexified = latexify(j, args)
    
    if isinstance(latexified, dict):
        if 'top-k-episodes' in latexified:
            print('Global top k episodes:', file=out)
            print('\n'.join(latexified['top-k-episodes']['global']), file=out)
            print('Per-size top k episodes:', file=out)
            print('\n'.join('{}-episodes:\n{}'.format(
                i, '\n'.join(str(e) for e in i_episodes)) for i, i_episodes in enumerate(latexified['top-k-episodes']['per-size'], start=1)), file=out)

        if 'top-k-rules' in latexified:
            print('Top k association rules:', file=out)
            print('\n'.join(latexified['top-k-rules']), file=out)

        print('All episodes:', file=out)
        print('\n'.join(latexified['episodes']), file=out)

    elif isinstance(latexified, list):
        print('\n'.join(latexified), file=out)

f.close()
if out is not sys.stdout: out.close()
