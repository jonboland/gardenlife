from pathlib import Path
import sys

# Enables gardenlife package imports when running tests
context = Path.cwd().parent / "gardenlife"
sys.path.insert(0, str(context))
