from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import numpy as np
import difflib

def calculate_cosine_similarity(text1, text2):
    vectorizer = TfidfVectorizer()
    tfidf = vectorizer.fit_transform([text1, text2])
    sim_matrix = cosine_similarity(tfidf[0:1], tfidf[1:2])
    return sim_matrix[0][0]

def label_similarity(similarity_score, threshold=0.8):
    return int(similarity_score >= threshold)

def highlight_matching_text(text1, text2):
    """
    Returns HTML-highlighted versions of text1 and text2 where matching blocks are marked.
    """
    matcher = difflib.SequenceMatcher(None, text1, text2)
    blocks = matcher.get_matching_blocks()

    def wrap_highlight(text, blocks, is_text1=True):
        result = []
        last_idx = 0
        for block in blocks:
            start = block.a if is_text1 else block.b
            length = block.size
            if length == 0:
                continue
            result.append(text[last_idx:start])
            result.append(f"<mark>{text[start:start+length]}</mark>")
            last_idx = start + length
        result.append(text[last_idx:])
        return ''.join(result)

    return wrap_highlight(text1, blocks, True), wrap_highlight(text2, blocks, False)