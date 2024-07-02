import sys
import os

# Ensure the project root (parent of bin/) is on the path
parent_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, parent_dir)

from myshell.core import main_loop

if __name__ == "__main__":
    main_loop()
