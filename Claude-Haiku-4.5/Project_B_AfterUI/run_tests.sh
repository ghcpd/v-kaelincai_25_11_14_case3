#!/bin/bash
# Run tests for Project B (After UI Improvement)

set -e

PROJECT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$PROJECT_DIR"

echo "========================================="
echo "Project B - After UI Improvement"
echo "========================================="
echo ""

# Activate virtual environment if it exists
if [ -d "venv" ]; then
    source venv/bin/activate
fi

# Start the web server in background
echo "Starting web server on http://localhost:3000..."
python3 src/server.py &
SERVER_PID=$!

# Give server time to start
sleep 2

# Run unit tests
echo ""
echo "Running unit tests..."
cd tests
python3 -m pytest test_post_unit.py -v --tb=short || true
cd ..

# Run E2E tests
echo ""
echo "Running E2E tests..."
cd tests
python3 test_post_e2e.py || true
cd ..

# Kill the server
kill $SERVER_PID 2>/dev/null || true

echo ""
echo "========================================="
echo "Tests completed!"
echo "Results saved to:"
echo "  - results/results_post.json"
echo "  - logs/log_post.txt"
echo "  - results/time_post.txt"
echo "Screenshots saved to:"
echo "  - screenshots/"
echo "========================================="
