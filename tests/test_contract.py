"""Tests for the published TruthLatch verification contract."""
import json
import unittest
from pathlib import Path

from jsonschema import Draft202012Validator, FormatChecker


ROOT = Path(__file__).resolve().parents[1]
SCHEMA_PATH = ROOT / "contracts" / "verification.schema.json"
EXAMPLES_DIR = ROOT / "contracts" / "examples"


class VerificationContractTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        with SCHEMA_PATH.open(encoding="utf-8") as file:
            cls.schema = json.load(file)

        cls.validator = Draft202012Validator(
            cls.schema,
            format_checker=FormatChecker(),
        )

    def load_example(self, filename):
        with (EXAMPLES_DIR / filename).open(encoding="utf-8") as file:
            return json.load(file)

    def test_verified_example_matches_schema(self):
        self.assertEqual(
            list(self.validator.iter_errors(self.load_example("verified.json"))),
            [],
        )

    def test_contradicted_example_matches_schema(self):
        self.assertEqual(
            list(self.validator.iter_errors(self.load_example("contradicted.json"))),
            [],
        )

    def test_unknown_example_matches_schema(self):
        self.assertEqual(
            list(self.validator.iter_errors(self.load_example("unknown.json"))),
            [],
        )

    def test_invalid_example_does_not_match_schema(self):
        self.assertNotEqual(
            list(self.validator.iter_errors(self.load_example("invalid.json"))),
            [],
        )


if __name__ == "__main__":
    unittest.main()
