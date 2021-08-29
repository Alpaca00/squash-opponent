from opponent_app import create_app
from opponent_app.models import TableResult, TableScore, Player
from opponent_app import db


positions = [1, 2, 3, 4]
teams = ["Anchors", "Warriors", "Snails", "Gladiators"]
points = [30, 29, 23, 14]
matches = [3, 3, 3, 3]
teams_compositions = [
    [
        """
1.Середович Юрій
2.Біляєв Остап
3.Мендзебровський Валентин
4.Батршин Олексій
"""
    ],
    [
        """
1.Шнейдер Дмитро
2.Нижник Роман
3.Шумельда Максим
4.Барсук Віталій(PSA)
5.Литвин Андріан"""
    ],
    [
        """
1.Кравс Юрій
2.Шеремет Михайло
3.Воськало Володимир
4.Мацьків Олег
"""
    ],
    [
        """
1.Завінський Ростислав
2.Томенчук Михайло
3.Стьопкін Євген
4.Семерак Максим
"""
    ],
]

dates = ["06.04.21", "06.19.21", "06.26.21", "07.04.21", "07.24.21", "08.01.21"]
scores = ["10:6", "9:7", "10:6", "12:4", "9:7", "12:4"]
teamsVS = [
    ["Snails", "Anchors", "Warriors", "Warriors", "Anchors", "Anchors"],
    ["Gladiators", "Warriors", "Snails", "Gladiators", "Snails", "Gladiators"],
]


def table_factory(position, team, point, match, team_composition):
    with create_app().app_context():
        r = TableResult(position=position, team=team, point=point, match=match)
        p = Player(full_name=team_composition)
        r.players.append(p)
        db.session.add(r)
        db.session.add(p)
        db.session.commit()


def table_result_factory(date, score, team1, team2):
    with create_app().app_context():
        s = TableScore(date=date, team1=team1, team2=team2, score=score)
        db.session.add(s)
        db.session.commit()


for i in range(0, 4):
    table_factory(
        positions[i],
        teams[i],
        point=points[i],
        match=matches[i],
        team_composition=teams_compositions[i],
    )

for i in range(0, 6):
    table_result_factory(
        date=dates[i], team1=teamsVS[0][i], team2=teamsVS[1][i], score=scores[i]
    )
