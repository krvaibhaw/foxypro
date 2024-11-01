import os
import json
import platform
import subprocess

# Path where aliases are saved between sessions
ALIAS_FILE = os.path.join(os.path.dirname(os.path.abspath(__file__)), "aliases.json")
