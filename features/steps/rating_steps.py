from behave import given, then, when

from tracker import Tracker


@given("результат матча «{home}» — «{away}» со счётом {home_goals:d}:{away_goals:d} внесён")
def record_match(context, home, away, home_goals, away_goals):
    if not hasattr(context, "tracker"):
        context.tracker = Tracker()
    context.tracker.add_result(home, away, home_goals, away_goals)


@when("запрашиваю рейтинг")
def request_rating(context):
    context.rating = [
        [str(place), row.team, str(row.points), str(row.goal_difference)]
        for place, row in context.tracker.rating()
    ]


@then("рейтинг содержит следующие строки по порядку")
def check_rating(context):
    expected = [row.cells for row in context.table]
    assert context.rating == expected, (context.rating, expected)
