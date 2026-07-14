"""Run r2d tests without unittest discover quirks."""
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[1] / 'src'))
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from tests import test_r2d
import unittest
result = unittest.TextTestRunner(verbosity=2).run(
    unittest.TestLoader().loadTestsFromModule(test_r2d)
)
sys.exit(0 if result.wasSuccessful() else 1)
