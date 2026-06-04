#!/usr/bin/env python3
import sys
import math

current_location = None
scores = []

def calculate_stats(scores):
    
    count = len(scores)
    mean = sum(scores) / count if count > 0 else 0
    
    
    if count > 1:
        variance = sum((x - mean) ** 2 for x in scores) / count
        std = math.sqrt(variance)
    else:
        std = 0.0
    
    return count, mean, std

for line in sys.stdin:
    line = line.strip()
    if not line:
        continue
    
    try:
        location, score_str = line.split('\t', 1)
        score = float(score_str)
    except ValueError:
        continue
    
    if location == current_location:
       
        scores.append(score)
    else:
        
        if current_location is not None and scores:
            count, mean, std = calculate_stats(scores)
            print(f"{current_location}\tCOUNT={count}\tMEAN={mean:.2f}\tSTD={std:.2f}")
        
        
        current_location = location
        scores = [score]


if current_location is not None and scores:
    count, mean, std = calculate_stats(scores)
    print(f"{current_location}\tCOUNT={count}\tMEAN={mean:.2f}\tSTD={std:.2f}")
