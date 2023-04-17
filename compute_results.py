
import os


raw_results = {}


for filename in os.listdir():
    if filename.startswith("results") and filename.endswith(".txt"):
        with open(filename) as file:
            lines = file.read().strip(" \n").split("\n")
            raw_results[filename] = lines


for name, res in raw_results.items():
    print(name)
    for score in map(str,[1, -1, 0.5, -0.5]):
        print("  ",score, " "*(5-len(score)), res.count(score))
        # print("res.count(score))