import numpy as np
import os

results_full = []
results_condensed = []

for filename in os.listdir():
    if filename.endswith(".out"):
        results = None
        with open(filename) as file:
            lines = file.read().split("\n")
        for line in lines[::-1]:
            if line.startswith("Results: ["):
                i = line.index("[")
                j = line.index("]")
                results = list(map(float, line[i+1:j].split(", ")))
                break
        assert results is not None, FileNotFoundError(f"no results in the file {filename}")
        if filename.startswith("generate_stats_short"): results_condensed += results
        elif filename.startswith("generate_stats"): results_full += results
        else: raise ValueError(f"filename {filename} is wierd")
        
def print_results(res, *args, **kwargs):
    scores = ["1   ","0.5 ","-0.5","-1  "]
    print(*args, **kwargs)
    for score in scores:
        print("  ", score, ":", res.count(float(score)))

print_results(results_full,"\ninitial_random_games=2,  n_expansions=200",)
print_results(results_condensed,"\ninitial_random_games=1,  n_expansions=20",)
                
            
