#!/bin/bash
set -e

echo "🐍 Running Pytest test runner... 🐍"
pytest tests -vv \
    --cov=. \
    --junitxml=junit/test-results.xml \
    --cov-report=xml \
    --cov-report=term \
    --cov-append

echo "🐍 Good to go! 🐍"