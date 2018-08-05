import sys
import argparse

parser = argparse.ArgumentParser()

parser.add_argument('i', nargs='?')
parser.add_argument('-o')

args = parser.parse_args()

fin = open(args.i) if args.i is not None else sys.stdin
fout = open(args.o) if args.o is not None else sys.stdout

output = [(float(line.split()[-1].split(';')[-2]), line) for line in fin.readlines()]

output.sort(key=lambda p: p[0], reverse=True)

print(''.join(o[1] for o in output), file=fout, end='')
