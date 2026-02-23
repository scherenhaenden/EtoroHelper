#!/usr/bin/env python3
"""
Test runner for EtoroHelper.
Installs test dependencies and runs pytest.
"""

import sys
import os

# Add src to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

from src.dependencies import install_test_dependencies

def main():
    print("Installing test dependencies...")
    install_test_dependencies()

    print("Running tests...")
    import subprocess
    result = subprocess.run([sys.executable, "-m", "pytest"], cwd=os.path.dirname(__file__))

    return result.returncode

if __name__ == "__main__":
    sys.exit(main())
