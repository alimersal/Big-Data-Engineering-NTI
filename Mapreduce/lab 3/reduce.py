#!/usr/bin/env python3
import sys

current_ip = None
current_count = 0

for line in sys.stdin:
    line = line.strip()
    if not line:
        continue
        
    try:
        ip, count = line.split('\t', 1)
        count = int(count)
    except ValueError:
        continue

    if current_ip == ip:
        current_count += count
    else:
        if current_ip is not None:
            print(f"{current_ip}\t{current_count}")
        current_ip = ip
        current_count = count


if current_ip is not None:
    print(f"{current_ip}\t{current_count}")
