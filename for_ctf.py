import argparse
import sys
from pathlib import Path

def line_matches(line: str) -> bool:
    # считаем только символы '0' и '1'
    zeros = line.count('0')
    ones  = line.count('1')
    return (zeros % 3 == 0) or (ones % 2 == 0)

def count_matching_lines(path: Path) -> int:
    total = 0
    with path.open('r', encoding='utf-8', errors='ignore') as f:
        for raw in f:
            line = raw.rstrip('\n\r')
            if line_matches(line):
                total += 1
    return total

def main():
    p = argparse.ArgumentParser(description="Count lines where #0 % 3 == 0 OR #1 % 2 == 0.")
    p.add_argument('file', help="Path to input file (use - for stdin)")
    args = p.parse_args()

    if args.file == '-':
        # работа со stdin
        total = 0
        for raw in sys.stdin:
            if line_matches(raw.rstrip('\n\r')):
                total += 1
        print(total)
        return

    path = Path(args.file)
    if not path.exists():
        print(f"File not found: {args.file}", file=sys.stderr)
        sys.exit(2)

    result = count_matching_lines(path)
    print(result)

if __name__ == '__main__':
    main()