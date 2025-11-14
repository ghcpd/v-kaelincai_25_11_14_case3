#!/bin/bash
# Run tests for Project A (Before UI Improvement)

set -e

PROJECT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$PROJECT_DIR"

echo "========================================="
echo "Project A - Before UI Improvement"
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
python3 -m pytest test_pre_unit.py -v --tb=short || true
cd ..

# Run E2E tests
echo ""
echo "Running E2E tests..."
cd tests
python3 test_pre_e2e.py || true
cd ..

# Kill the server
kill $SERVER_PID 2>/dev/null || true

echo ""
echo "========================================="
echo "Tests completed!"
echo "Results saved to:"
echo "  - results/results_pre.json"
echo "  - logs/log_pre.txt"
echo "  - results/time_pre.txt"
echo "Screenshots saved to:"
echo "  - screenshots/"
echo "========================================="
