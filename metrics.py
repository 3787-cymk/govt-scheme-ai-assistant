# Example relevance list (1 = relevant result, 0 = not relevant)
results = [1, 0, 1, 0, 1]

# Precision
precision = sum(results) / len(results)

# Assume total relevant schemes in dataset
total_relevant = 6
recall = sum(results) / total_relevant

# MRR
first_relevant_rank = results.index(1) + 1
mrr = 1 / first_relevant_rank

print("Precision:", precision)
print("Recall:", recall)
print("MRR:", mrr)

