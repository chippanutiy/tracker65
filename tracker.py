from dataclasses import dataclass, replace


@dataclass(frozen=True)
class TeamRow:
    team: str
    played: int = 0
    wins: int = 0
    draws: int = 0
    losses: int = 0
    goals_for: int = 0
    goals_against: int = 0
    points: int = 0

    @property
    def goal_difference(self):
        return self.goals_for - self.goals_against

    def after_match(self, scored, conceded):
        won = scored > conceded
        drew = scored == conceded
        lost = scored < conceded
        return replace(
            self,
            played=self.played + 1,
            wins=self.wins + won,
            draws=self.draws + drew,
            losses=self.losses + lost,
            goals_for=self.goals_for + scored,
            goals_against=self.goals_against + conceded,
            points=self.points + 3 * won + drew,
        )


class Tracker:
    def __init__(self):
        self._rows = {}

    def add_result(self, home, away, home_goals, away_goals):
        home, away = home.strip(), away.strip()
        if not home or not away:
            raise ValueError("названия команд должны быть непустыми.")
        if home == away:
            raise ValueError("в матче должны участвовать разные команды.")
        if any("|" in name or not name.isprintable() for name in (home, away)):
            raise ValueError("в названии команды недопустимы символ | и управляющие символы.")
        if any(type(goals) is not int or goals < 0 for goals in (home_goals, away_goals)):
            raise ValueError("счёт должен состоять из неотрицательных целых чисел.")

        home_row = self._rows.get(home, TeamRow(home))
        away_row = self._rows.get(away, TeamRow(away))
        self._rows[home] = home_row.after_match(home_goals, away_goals)
        self._rows[away] = away_row.after_match(away_goals, home_goals)

    def table(self):
        return tuple(self._rows[name] for name in sorted(self._rows, key=team_name_key))

    def rating(self):
        ordered = sorted(self._rows.values(), key=rating_key)
        return tuple(enumerate(ordered, start=1))


def team_name_key(name):
    return name.casefold(), name


def rating_key(row):
    return -row.points, -row.goal_difference, -row.goals_for, team_name_key(row.team)


def print_table(rows):
    if not rows:
        print("Результатов пока нет.")
        return

    print("Команда | И | В | Н | П | ЗМ | ПМ | РМ | О")
    for row in rows:
        print(f"{row.team} | {row.played} | {row.wins} | {row.draws} | "
              f"{row.losses} | {row.goals_for} | {row.goals_against} | "
              f"{row.goal_difference:+d} | {row.points}")


def print_rating(rating):
    if not rating:
        print("Результатов пока нет.")
        return

    print("Место | Команда | Очки | Разница мячей")
    for place, row in rating:
        print(f"{place} | {row.team} | {row.points} | {row.goal_difference:+d}")


def read_score():
    home_text = input("Голы первой команды: ")
    away_text = input("Голы второй команды: ")
    try:
        return int(home_text), int(away_text)
    except ValueError as error:
        raise ValueError("счёт должен состоять из целых чисел.") from error


def main():
    tracker = Tracker()
    print("Трекер спортивных результатов")
    try:
        while True:
            print("\n1. Добавить результат\n2. Таблица результатов\n3. Рейтинг\n0. Выход")
            choice = input("Выберите пункт: ").strip()
            if choice == "0":
                return
            if choice == "1":
                try:
                    home = input("Первая команда: ")
                    away = input("Вторая команда: ")
                    home_goals, away_goals = read_score()
                    tracker.add_result(home, away, home_goals, away_goals)
                    print("Результат добавлен.")
                except ValueError as error:
                    print(f"Ошибка: {error}")
            elif choice == "2":
                print_table(tracker.table())
            elif choice == "3":
                print_rating(tracker.rating())
            else:
                print("Выберите пункт 0, 1, 2 или 3.")
    except (EOFError, KeyboardInterrupt):
        print()


if __name__ == "__main__":
    main()
