from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import numpy as np

def calculate_cosine_similarity(text1, text2):
    vectorizer = TfidfVectorizer()
    tfidf = vectorizer.fit_transform([text1, text2])
    sim_matrix = cosine_similarity(tfidf[0:1], tfidf[1:2])
    return sim_matrix[0][0]

def label_similarity(similarity_score, threshold=0.8):
    return int(similarity_score >= threshold)