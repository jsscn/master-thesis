import argparse
import sys
import json

parser = argparse.ArgumentParser()

parser.add_argument('-i')
parser.add_argument('-o')
parser.add_argument('--no-singletons', action='store_true')
parser.add_argument('--filter', type=int)
parser.add_argument('--rank', action='store_true')
parser.add_argument('--top-k', type=int)
parser.add_argument('--episodes-only', action='store_true')
parser.add_argument('--rules-only', action='store_true')

args = parser.parse_args()

fin = open(args.i) if args.i is not None else sys.stdin
fout = open(args.o) if args.o is not None else sys.stdout

j = json.load(fin)

any_rules = not args.episodes_only and j.get('association-rules') is not None

if not args.rules_only:
    episodes = j['episodes']

    if args.no_singletons:
        episodes = [episode for episode in episodes if len(episode['event-types']) > 1]

    if args.filter is not None:
        episodes = [episode for episode in episodes if len(episode['event-types']) == args.filter]

    if args.rank or args.top_k:
        episodes.sort(key=lambda episode: episode['frequency'], reverse=True)

        if args.top_k is not None:
            episodes = episodes[:args.top_k]

if any_rules:
    rules = j['association-rules']

    if args.rank or args.top_k:
        rules.sort(key=lambda rule: rule['confidence', reverse=True])

    if args.top_k is not None:
        rules = rules[:args.top_k]



if any_rules:
    json.dump({'episodes': episodes, 'association-rules': rules}, fout, indent=2)
elif rules_only:
    json.dump(rules, fout, indent=2)
else:
    json.dump(episodes, fout, indent=2)

if fin is not sys.stdin: fin.close()
if fout is not sys.stdout: fout.close()
