# test_requests.py
import requests
with open("sample_data/original.txt","rb") as f1, open("sample_data/submission.txt","rb") as f2:
    files = {
        "original": ("original.txt", f1.read(), "text/plain"),
        "submission": ("submission.txt", f2.read(), "text/plain")
    }
    r = requests.post("http://127.0.0.1:5000/check", files=files)
    print(r.status_code)
    print(r.text)
