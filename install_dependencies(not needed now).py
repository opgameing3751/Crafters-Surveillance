import os
import sys
import subprocess
import argparse

# ANSI color codes
GREEN = "\033[32m"
YELLOW = "\033[33m"
RED = "\033[31m"
RESET = "\033[0m"

# List of required packages
required_packages = ["requests", "python-dotenv"]

def install_package(package, break_system_packages=False):
    """Install a package using pip, optionally with --break-system-packages."""
    try:
        command = [sys.executable, "-m", "pip", "install", package]
        if break_system_packages:
            command.append("--break-system-packages")
        
        subprocess.check_call(command)
        print(f"{GREEN}Successfully installed: {package}{RESET}")
    except subprocess.CalledProcessError:
        print(f"{RED}Failed to install: {package}{RESET}")

def main():
    """Parse arguments, check, and install required packages."""
    parser = argparse.ArgumentParser(description="Install required Python packages.")
    parser.add_argument("--break-system-packages", action="store_true",
                        help="Allow installation that modifies system packages.")
    args = parser.parse_args()

    for package in required_packages:
        try:
            __import__(package)
            print(f"{GREEN}{package} is already installed.{RESET}")
        except ImportError:
            print(f"{YELLOW}Installing {package}...{RESET}")
            install_package(package, args.break_system_packages)

if __name__ == "__main__":
    main()