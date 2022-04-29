import datetime
import sqlalchemy
from .db_session import SqlAlchemyBase
from sqlalchemy import orm


class Suggetions(SqlAlchemyBase):
    __tablename__ = 'suggetions'

    id = sqlalchemy.Column(sqlalchemy.Integer,
                           primary_key=True, autoincrement=True)
    date = sqlalchemy.Column(sqlalchemy.Date, nullable=datetime.date.today())
    name = sqlalchemy.Column(sqlalchemy.String, nullable=True)