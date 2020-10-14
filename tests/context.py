from pathlib import Path
import sys

# Enables gardenlife package imports when running tests
context = Path(__file__).resolve().parents[1] / "gardenlife"
sys.path.insert(0, str(context))
