from copy import deepcopy

results = {
                    'r': (1.0, 1.0), 
                    'b': (2.0, 2.0),
                    'g': (3.0, 3.0),
                    'y': (4.0, 4.0),
                    'p': (5.0, 5.0)
        }

list = []

for items in results:
    results[items] = deepcopy((results[items][0] / 10, results[items][1] / 10))

print(results)
