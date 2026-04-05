#!/usr/bin/env python
"""
Test runner for Image to Prompt node tests.
Run this script from the project root directory.

Usage:
    python run_tests.py                    # Run all tests
    python run_tests.py -v                 # Verbose output
    python run_tests.py --cov              # With coverage
"""

import subprocess
import sys
from pathlib import Path

def run_tests():
    """Run pytest on the tests directory"""
    # Get the project root (where this script is located)
    project_root = Path(__file__).parent
    tests_dir = project_root / "tests"
    
    # Build pytest command
    cmd = [
        sys.executable,
        "-m",
        "pytest",
        str(tests_dir),
        "-v",
        "--tb=short",
        *sys.argv[1:]  # Pass through any additional arguments
    ]
    
    print(f"Running tests from: {tests_dir}")
    print(f"Command: {' '.join(cmd)}")
    print("-" * 70)
    
    result = subprocess.run(cmd, cwd=project_root)
    return result.returncode

if __name__ == "__main__":
    sys.exit(run_tests())
