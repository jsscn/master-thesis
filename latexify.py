import sys
import argparse

parser = argparse.ArgumentParser()

parser.add_argument("-c", type=str, default="parallel") # parallel or serial (parallel by default, I guess)
parser.add_argument("-f", type=str)
parser.add_argument("-o", type=str)
parser.add_argument("--math-mode-delimiters", action="store_true")
parser.add_argument("--regular-text", action="store_true")
parser.add_argument("--frequencies", action="store_true")

args = parser.parse_args()


f = sys.stdin if args.f is None else open(args.f)
out = sys.stdout if args.o is None else open(args.o, "w")

for line in f:
    if ":" in line: continue

    elements = line.split()[:-1]
    frequency = float(line.split()[-1][1:-1])

    elements_it = ("\\text{{{}}}".format(e) for e in elements) if args.regular_text \
        else elements

    if args.c == "parallel":
        latexified = "\\{{ {} \\}}".format(", ".join(elements_it))
    else:
        latexified = " \\to ".join(elements_it)

    if args.math_mode_delimiters:
        latexified = "$ {} $".format(latexified)

    if args.frequencies:
        latexified = "{} ({:.3g})".format(latexified, frequency)

    print(latexified, file=out)


f.close()
out.close()
