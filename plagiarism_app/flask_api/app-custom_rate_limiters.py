# flask_api/app.py
from flask import Flask, request, jsonify
import threading
import time
import joblib

from utils import calculate_cosine_similarity, highlight_matching_text

app = Flask(__name__)
model = joblib.load("plagiarism_model.pkl")

# ---------------- Rate limiters Implementation ----------------

class TokenBucket:
    def __init__(self, capacity, refill_rate):
        self.capacity = float(capacity)
        self.tokens = float(capacity)
        self.refill_rate = float(refill_rate)
        self.last = time.monotonic()
        self.lock = threading.Lock()

    def _refill(self):
        now = time.monotonic()
        elapsed = now - self.last
        if elapsed > 0:
            self.tokens = min(self.capacity, self.tokens + elapsed * self.refill_rate)
            self.last = now

    def consume(self, amount=1.0):
        with self.lock:
            self._refill()
            if self.tokens >= amount:
                self.tokens -= amount
                return True
            return False

class LeakyBucket:
    def __init__(self, capacity, leak_rate):
        self.capacity = float(capacity)
        self.level = 0.0
        self.leak_rate = float(leak_rate)
        self.last = time.monotonic()
        self.lock = threading.Lock()

    def _leak(self):
        now = time.monotonic()
        elapsed = now - self.last
        if elapsed > 0:
            leaked = elapsed * self.leak_rate
            self.level = max(0.0, self.level - leaked)
            self.last = now

    def allow(self, weight=1.0):
        with self.lock:
            self._leak()
            if (self.level + weight) <= self.capacity:
                self.level += weight
                return True
            return False

# simple in-memory store (per-client)
_bucket_store = {}
_store_lock = threading.Lock()

def get_token_bucket(key, capacity, refill_rate):
    with _store_lock:
        b = _bucket_store.get(key)
        if not isinstance(b, TokenBucket):
            b = TokenBucket(capacity, refill_rate)
            _bucket_store[key] = b
        return b

def get_leaky_bucket(key, capacity, leak_rate):
    with _store_lock:
        b = _bucket_store.get(key)
        if not isinstance(b, LeakyBucket):
            b = LeakyBucket(capacity, leak_rate)
            _bucket_store[key] = b
        return b

# ---------------- Configuration (adjust for demo) ----------------
# Set ALGO = "token" or "leaky"
ALGO = "leaky"   # "token" or "leaky"

# Token bucket params
TOKEN_CAPACITY = 3
TOKEN_REFILL_PER_SEC = 0.5

# Leaky bucket params
LEAK_CAPACITY = 3
LEAK_PER_SEC = 1.5

def client_key(req):
    # use X-Forwarded-For when behind a proxy like Kong, otherwise remote_addr
    return req.headers.get("X-Forwarded-For", req.remote_addr or "unknown")

def is_allowed(req):
    key = client_key(req)
    if ALGO == "token":
        b = get_token_bucket(key, TOKEN_CAPACITY, TOKEN_REFILL_PER_SEC)
        allowed = b.consume(1.0)
        return allowed
    else:
        b = get_leaky_bucket(key, LEAK_CAPACITY, LEAK_PER_SEC)
        allowed = b.allow(1.0)
        return allowed

# ---------------- Endpoint ----------------

@app.route("/check", methods=["POST"])
def check():
    # rate limit check (minimal)
    if not is_allowed(request):
        return jsonify({"error": "Too Many Requests"}), 429

    file1 = request.files['original']
    file2 = request.files['submission']
    text1 = file1.read().decode("utf-8")
    text2 = file2.read().decode("utf-8")

    similarity = calculate_cosine_similarity(text1, text2)
    prediction = model.predict([[similarity]])[0]
    probability = model.predict_proba([[similarity]])[0][1]
    highlight1, highlight2 = highlight_matching_text(text1, text2)

    return jsonify({
        "similarity_score": round(similarity, 4),
        "plagiarized": bool(prediction),
        "probability": round(probability, 4),
        "highlighted_original": highlight1,
        "highlighted_submission": highlight2
    })

if __name__ == "__main__":
    app.run(debug=True, port=5001)
