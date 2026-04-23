"""
main.py — Entry point for University Management System
"""

import sys
import os


sys.path.insert(0, os.path.dirname(__file__))

from ui import ConsoleUI


def main():
    app = ConsoleUI()
    app.run()


if __name__ == "__main__":
    main()
