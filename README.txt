Практическая работа 3. Вариант 65
Трекер спортивных результатов

Распакуйте архив и откройте папку Tracker65 в VS Code.
Программа требует Python 3.10 или новее. Для запуска дополнительные пакеты не нужны.
Данные хранятся в памяти до закрытия программы.

Запуск на Windows из PowerShell:
    py -3 -X utf8 tracker.py

Тесты на Windows:
    py -3 -m venv .venv
    .\.venv\Scripts\python.exe -m pip install -r requirements.txt
    .\.venv\Scripts\python.exe -X utf8 -m unittest discover -s tests -v
    .\.venv\Scripts\python.exe -X utf8 -m behave --no-color --format plain

Команды для Linux/macOS:
    python3 -X utf8 tracker.py
    python3 -m venv .venv
    .venv/bin/python -m pip install -r requirements.txt
    .venv/bin/python -X utf8 -m unittest discover -s tests -v
    .venv/bin/python -X utf8 -m behave --no-color --format plain

Пункты меню: 1 — добавить результат, 2 — таблица, 3 — рейтинг, 0 — выход.
Демо: Сокол — Вымпел 2:0, затем Рубин — Сокол 1:1.
Ожидаемый рейтинг по очкам: Сокол (4), Рубин (1), Вымпел (0).

tracker.py — исходный код программы.
tests/ — проверки TDD, ATDD и SDD.
features/ — сценарии BDD и их реализация через Behave.
spec/ — табличная спецификация SDD.
evidence/ — журналы разработки, итоговых запусков и демонстрации.
