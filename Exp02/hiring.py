from itertools import permutations
import random
def get_permutations(candidate):
    random_candidates = list(permutations(candidate))[0]
    print("Candidates: ",random_candidates)
    return random_candidates


best = 0
# current candidates
candidates = [random.randint(1,11) for _ in range(10)]
# randomized
randomized_candidates = get_permutations(candidates)
best_candidates = []
count_hired = 0
for i in range(len(candidates)):
    if randomized_candidates[i] > best:
        best = randomized_candidates[i]
        best_candidates.append(best)
        count_hired += 1

print("Hired Candidates: ",best_candidates)
print("Total Hired: ",count_hired)
print("Total Fired: ",count_hired - 1)
