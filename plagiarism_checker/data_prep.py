import pandas as pd
from utils import calculate_cosine_similarity

# Simulated training data
data = [
    ("This is the original sentence.", "This is the original sentence.", 1),
    ("The sky is blue and beautiful.", "The sky is blue.", 1),
    ("Machine learning is fun.", "I like pizza.", 0),
    ("Python is a great language.", "I use Java for backend.", 0),
]

# Compute similarity and label
rows = []
for original, submission, label in data:
    sim = calculate_cosine_similarity(original, submission)
    rows.append([original, submission, sim, label])

df = pd.DataFrame(rows, columns=["Original", "Submission", "Similarity", "Label"])
df.to_csv("plagiarism_dataset.csv", index=False)