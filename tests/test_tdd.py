import unittest

from tracker import Tracker


class TableUpdateTests(unittest.TestCase):
    def setUp(self):
        self.tracker = Tracker()

    def test_win_updates_both_teams(self):
        self.tracker.add_result("Сокол", "Вымпел", 3, 1)
        rows = {row.team: row for row in self.tracker.table()}
        winner = rows["Сокол"]
        loser = rows["Вымпел"]
        self.assertEqual((winner.played, winner.wins, winner.draws, winner.losses,
                          winner.goals_for, winner.goals_against, winner.points),
                         (1, 1, 0, 0, 3, 1, 3))
        self.assertEqual((loser.played, loser.wins, loser.draws, loser.losses,
                          loser.goals_for, loser.goals_against, loser.points),
                         (1, 0, 0, 1, 1, 3, 0))

    def test_draw_updates_both_teams(self):
        self.tracker.add_result("Сокол", "Вымпел", 0, 0)
        for row in self.tracker.table():
            self.assertEqual((row.played, row.draws, row.points), (1, 1, 1))
        self.assertEqual(len(self.tracker.table()), 2)

    def test_second_match_accumulates_statistics(self):
        self.tracker.add_result("Сокол", "Вымпел", 2, 0)
        self.tracker.add_result("Рубин", "Сокол", 4, 1)
        row = next(row for row in self.tracker.table() if row.team == "Сокол")
        self.assertEqual((row.played, row.wins, row.losses, row.goals_for,
                          row.goals_against, row.points), (2, 1, 1, 3, 4, 3))

    def test_invalid_result_keeps_table(self):
        self.tracker.add_result("Сокол", "Вымпел", 2, 0)
        before = self.tracker.table()
        invalid = [
            ("Сокол", "Рубин", -1, 0),
            ("Сокол", " Сокол ", 2, 0),
            ("", "Рубин", 2, 0),
            ("Сокол", "Рубин", 1.5, 0),
            ("Сокол", "Рубин", True, 0),
            ("Сокол | А", "Рубин", 2, 0),
        ]
        for args in invalid:
            with self.subTest(args=args):
                with self.assertRaises(ValueError):
                    self.tracker.add_result(*args)
                self.assertEqual(self.tracker.table(), before)
