import pandas as pd
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import train_test_split
import joblib

# Load data
df = pd.read_csv("plagiarism_dataset.csv")

X = df[['Similarity']]
y = df['Label']

# Split and train
X_train, X_test, y_train, y_test = train_test_split(X, y, random_state=42)
model = LogisticRegression()
model.fit(X_train, y_train)

# Save model
joblib.dump(model, 'plagiarism_model.pkl')