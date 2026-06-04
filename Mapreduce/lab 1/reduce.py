import sys
from collections import defaultdict

def main():
    counts = defaultdict(int)
    
    for line in sys.stdin:
        line = line.strip()
        if not line:
            continue
        try:
            fruit, count = line.split('\t', 1)
            counts[fruit] += int(count)
        except ValueError:
            continue


    for fruit in sorted(counts.keys()):
        print(f"{fruit}\t{counts[fruit]}")

if __name__ == "__main__":
    main()
