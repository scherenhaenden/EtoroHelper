import importlib
import subprocess
import sys

def install_if_not_exists(package, import_name=None):
    """
    Installs a package if it's not already installed.
    """
    if import_name is None:
        import_name = package
    try:
        importlib.import_module(import_name)
        return  # Package is already installed
    except ImportError:
        print(f"Could not find '{import_name}'. Attempting to install '{package}'.")

    try:
        # Try to install the package using pip
        subprocess.check_call([sys.executable, "-m", "pip", "install", package])
        print(f"Successfully installed '{package}'.")
    except subprocess.CalledProcessError:
        print("Failed to install with pip. This might be because pip is not installed.")
        print("Attempting to bootstrap pip and retry.")
        try:
            import ensurepip
            ensurepip.bootstrap()
            print("pip bootstrapped. Retrying package installation.")
            subprocess.check_call([sys.executable, "-m", "pip", "install", package])
            print(f"Successfully installed '{package}'.")
        except Exception as bootstrap_error:
            print(f"Failed to bootstrap pip and install '{package}'. Error: {bootstrap_error}", file=sys.stderr)
            print("Please ensure your Python environment is correctly set up with pip.", file=sys.stderr)
            sys.exit(1)

def install_dependencies():
    install_if_not_exists("beautifulsoup4", "bs4")
    install_if_not_exists("requests")
    install_if_not_exists("selenium")
    install_if_not_exists("webdriver-manager")

def install_test_dependencies():
    """Install dependencies needed for testing."""
    install_if_not_exists("pytest")
