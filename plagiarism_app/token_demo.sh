# token_demo.sh
# set ALGO=token in app.py then run this
for i in $(seq 1 6); do
  curl -s -o /dev/null -w "%{http_code} " \
    -X POST "http://localhost:5001/check" \
    -F "original=@sample_data/original.txt" \
    -F "submission=@sample_data/submission.txt"
done; echo