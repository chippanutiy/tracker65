import subprocess
import sys
import unittest
from pathlib import Path


def run_program(*answers):
    script = Path(__file__).resolve().parents[1] / "tracker.py"
    result = subprocess.run(
        [sys.executable, "-X", "utf8", str(script)],
        input="\n".join(answers) + "\n",
        encoding="utf-8",
        capture_output=True,
        timeout=5,
        check=True,
    )
    return result.stdout


class AcceptanceTests(unittest.TestCase):
    def test_table_is_current_after_each_match(self):
        output = run_program(
            "1", "Сокол", "Вымпел", "2", "0", "2",
            "1", "Рубин", "Сокол", "1", "1", "2", "3", "0",
        )
        first, second = output.split("Команда | И | В | Н | П | ЗМ | ПМ | РМ | О\n")[1:]
        self.assertIn("Сокол | 1 | 1 | 0 | 0 | 2 | 0 | +2 | 3\n", first)
        self.assertIn("Вымпел | 1 | 0 | 0 | 1 | 0 | 2 | -2 | 0\n", first)
        self.assertNotIn("Рубин |", first)
        self.assertIn("Сокол | 2 | 1 | 1 | 0 | 3 | 1 | +2 | 4\n", second)
        self.assertIn("Рубин | 1 | 0 | 1 | 0 | 1 | 1 | +0 | 1\n", second)
        self.assertIn("Вымпел | 1 | 0 | 0 | 1 | 0 | 2 | -2 | 0\n", second)
        self.assertIn("1 | Сокол | 4 | +2\n2 | Рубин | 1 | +0\n3 | Вымпел | 0 | -2\n", second)

    def test_bad_score_reports_error_and_keeps_table(self):
        output = run_program(
            "1", "Сокол", "Вымпел", "2", "0",
            "1", "Рубин", "Сокол", "abc", "1", "2", "0",
        )
        self.assertEqual(output.count("Результат добавлен."), 1)
        self.assertIn("Ошибка: счёт должен состоять из целых чисел.", output)
        self.assertIn("Сокол | 1 | 1 | 0 | 0 | 2 | 0 | +2 | 3\n", output)
        self.assertNotIn("Рубин |", output)

    def test_empty_views_have_a_message(self):
        output = run_program("2", "3", "0")
        self.assertEqual(output.count("Результатов пока нет."), 2)
