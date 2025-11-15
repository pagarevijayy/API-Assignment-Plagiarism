# leaky_demo.sh
# set ALGO=leaky in app.py then run this
echo "Burst:"
for i in $(seq 1 6); do \
  curl -s -o /dev/null -w "%{http_code} " \
    -X POST "http://localhost:5001/check" \
    -F "original=@sample_data/original.txt" \
    -F "submission=@sample_data/submission.txt"; \
done; echo

sleep 2

echo "Steady (sleep 2s):"
for i in $(seq 1 6); do \
  curl -s -o /dev/null -w "%{http_code} " \
    -X POST "http://localhost:5001/check" \
    -F "original=@sample_data/original.txt" \
    -F "submission=@sample_data/submission.txt"; \
  sleep 2; \
done; echo
