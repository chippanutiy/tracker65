import json
import unittest
from pathlib import Path

from tracker import Tracker


class RatingExamplesTests(unittest.TestCase):
    def test_rating_from_specification(self):
        spec = Path(__file__).resolve().parents[1] / "spec" / "rating_examples.json"
        examples = json.loads(spec.read_text(encoding="utf-8"))

        for example in examples:
            with self.subTest(example=example["example"]):
                tracker = Tracker()
                for match in example["matches"]:
                    tracker.add_result(*match)
                actual = [
                    [place, row.team, row.points, row.goal_difference]
                    for place, row in tracker.rating()
                ]
                self.assertEqual(actual, example["rating"])
