#!/usr/bin/env python3
"""Test runner script with different test categories."""

import sys
import subprocess
from pathlib import Path


def run_unit_tests():
    """Run unit tests only (no API calls)."""
    print("Running unit tests...")
    cmd = [
        sys.executable, "-m", "pytest", 
        "tests/test_config.py", 
        "tests/test_fred_client.py",
        "-v", "--tb=short"
    ]
    return subprocess.run(cmd).returncode


def run_integration_tests():
    """Run integration tests (requires API key and internet)."""
    print("Running integration tests...")
    print("Note: These tests require a valid FRED API key and internet connection.")
    
    cmd = [
        sys.executable, "-m", "pytest", 
        "tests/test_fred_integration.py",
        "-v", "--tb=short", "-s"
    ]
    return subprocess.run(cmd).returncode


def run_all_tests():
    """Run all tests."""
    print("Running all tests...")
    cmd = [
        sys.executable, "-m", "pytest", 
        "tests/",
        "-v", "--tb=short"
    ]
    return subprocess.run(cmd).returncode


def main():
    """Main test runner."""
    if len(sys.argv) < 2:
        print("Usage: python run_tests.py [unit|integration|all]")
        print("  unit        - Run unit tests only (fast, no API calls)")
        print("  integration - Run integration tests (requires API key)")
        print("  all         - Run all tests")
        sys.exit(1)
    
    test_type = sys.argv[1].lower()
    
    if test_type == "unit":
        exit_code = run_unit_tests()
    elif test_type == "integration":
        exit_code = run_integration_tests()
    elif test_type == "all":
        exit_code = run_all_tests()
    else:
        print(f"Unknown test type: {test_type}")
        sys.exit(1)
    
    sys.exit(exit_code)


if __name__ == "__main__":
    main()