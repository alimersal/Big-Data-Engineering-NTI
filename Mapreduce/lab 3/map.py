#!/usr/bin/env python3
import sys

for line in sys.stdin:
    line = line.strip()
    if not line:
        continue
    ip = line.split()[0]
    print(f"{ip}\t1")
