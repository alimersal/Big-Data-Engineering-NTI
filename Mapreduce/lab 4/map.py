#!/usr/bin/env python3
import sys

for line in sys.stdin:
    line = line.strip()
    if not line:
        continue
    
    try:
        
        parts = line.split('***')
        if len(parts) < 2:
            continue
        
        score = float(parts[0].strip())
        location = parts[1].strip()  # CHINA_Beijing أو PRC_Anhui
        
        
        print(f"{location}\t{score}")
        
    except (ValueError, IndexError):
        continue
