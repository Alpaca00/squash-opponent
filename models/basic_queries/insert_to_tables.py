from app import app
from models import db, TableResult, TableScore, Player

positions = [1, 2, 3, 4]
teams = ["Warriors", "Snails", "Anchors", "Gladiators"]
points = [29, 23, 18, 10]
matches = [3, 3, 2, 2]
teams_compositions = [
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
1.Середович Юрій
2.Біляєв Остап
3.Мендзебровський Валентин
4.Батршин Олексій
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

dates = ["06.04.21", "06.19.21", "06.26.21", "07.04.21", "07.24.21"]
scores = ["10:6", "9:7", "10:6", "12:4", "9:7"]
teamsVS = [
    ["Snails", "Anchors", "Warriors", "Warriors", "Anchors"],
    ["Gladiators", "Warriors", "Snails", "Gladiators", "Snails"],
]


def table_factory(position, team, point, match, team_composition):
    with app.app_context():
        r = TableResult(position=position, team=team, point=point, match=match)
        p = Player(full_name=team_composition)
        r.players.append(p)
        db.session.add(r)
        db.session.add(p)
        db.session.commit()


def table_result_factory(date, score, team1, team2):
    with app.app_context():
        s = TableScore(date=date, team1=team1, team2=team2, score=score)
        db.session.add(s)
        db.session.commit()


# for i in range(0, 4):
#     table_factory(
#         positions[i],
#         teams[i],
#         point=points[i],
#         match=matches[i],
#         team_composition=teams_compositions[i],
#     )

for i in range(0, 5):
    table_result_factory(
        date=dates[i], team1=teamsVS[0][i], team2=teamsVS[1][i], score=scores[i]
    )

