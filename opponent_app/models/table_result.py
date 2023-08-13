from sqlalchemy import Column, Date, ForeignKey, Integer, String, Text

from opponent_app.models import db


class TableResult(db.Model):
    """TableResult model for storing table results."""
    __tablename__ = "table_results"  # noqa
    id = Column(Integer, primary_key=True)
    position = Column(Integer, nullable=False)
    team = Column(String, nullable=False)
    point = Column(Integer, nullable=False)
    match = Column(String, nullable=False)
    players = db.relationship("Player", backref="table_results", lazy="joined")


class TableScore(db.Model):
    """TableScore model for storing table scores."""
    __tablename__ = "table_scores"  # noqa
    id = Column(Integer, primary_key=True)
    date = Column(Date, nullable=False)
    team1 = Column(String, nullable=False)
    team2 = Column(String, nullable=False)
    score = Column(String, nullable=False)


class Player(db.Model):
    """Player model for storing players."""
    __tablename__ = "players"  # noqa
    id = Column(Integer, primary_key=True)
    full_name = Column(Text, nullable=False)
    table_result_id = Column(Integer, ForeignKey("table_results.id"))
    table_result = db.relationship(
        "TableResult", overlaps="players,table_results"
    )
