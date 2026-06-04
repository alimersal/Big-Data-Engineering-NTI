#!/usr/bin/env python3
import sys
import re


if hasattr(sys.stdin, 'reconfigure'):
    sys.stdin.reconfigure(encoding='utf-8')

for line in sys.stdin:
    line = line.strip()
    if not line:
        continue


    words = re.findall(r"\b[a-z']+\b", line.lower())

    for word in words:

        word = word.strip("'")

        if len(word) >= 2:
            print(f"{word}\t1")
