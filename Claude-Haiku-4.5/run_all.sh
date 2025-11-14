#!/bin/bash
# Master script to run all tests for Project A and Project B
# Generates comparison report and aggregates results

set -e

REPO_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
RESULTS_DIR="$REPO_ROOT/results"
PROJECT_A_DIR="$REPO_ROOT/Project_A_BeforeUI"
PROJECT_B_DIR="$REPO_ROOT/Project_B_AfterUI"

# Create results directory
mkdir -p "$RESULTS_DIR"

echo "========================================="
echo "UI/UX Improvement Evaluation"
echo "========================================="
echo ""

# Run Project A tests
echo "Running Project A (Before) tests..."
cd "$PROJECT_A_DIR"
bash run_tests.sh
cd "$REPO_ROOT"

echo ""
echo "Project A tests completed!"
echo ""

# Run Project B tests
echo "Running Project B (After) tests..."
cd "$PROJECT_B_DIR"
bash run_tests.sh
cd "$REPO_ROOT"

echo ""
echo "Project B tests completed!"
echo ""

# Copy results to aggregated results folder
echo "Aggregating results..."
cp "$PROJECT_A_DIR/results/results_pre.json" "$RESULTS_DIR/" 2>/dev/null || echo "Note: results_pre.json not found"
cp "$PROJECT_A_DIR/results/time_pre.txt" "$RESULTS_DIR/" 2>/dev/null || echo "Note: time_pre.txt not found"
cp "$PROJECT_A_DIR/logs/log_pre.txt" "$RESULTS_DIR/" 2>/dev/null || echo "Note: log_pre.txt not found"

cp "$PROJECT_B_DIR/results/results_post.json" "$RESULTS_DIR/" 2>/dev/null || echo "Note: results_post.json not found"
cp "$PROJECT_B_DIR/results/time_post.txt" "$RESULTS_DIR/" 2>/dev/null || echo "Note: time_post.txt not found"
cp "$PROJECT_B_DIR/logs/log_post.txt" "$RESULTS_DIR/" 2>/dev/null || echo "Note: log_post.txt not found"

# Generate comparison report
python3 "$REPO_ROOT/generate_comparison_report.py"

echo ""
echo "========================================="
echo "Evaluation Complete!"
echo "========================================="
echo ""
echo "Generated artifacts:"
echo "  - results/results_pre.json (Before)"
echo "  - results/results_post.json (After)"
echo "  - results/time_pre.txt"
echo "  - results/time_post.txt"
echo "  - results/log_pre.txt"
echo "  - results/log_post.txt"
echo "  - compare_report.md (Comparison)"
echo ""
echo "Screenshots:"
echo "  - Project_A_BeforeUI/screenshots/"
echo "  - Project_B_AfterUI/screenshots/"
echo ""
