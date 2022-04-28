import datetime
import sqlalchemy
from .db_session import SqlAlchemyBase
from sqlalchemy import orm


class Films(SqlAlchemyBase):
    __tablename__ = 'films'

    id = sqlalchemy.Column(sqlalchemy.Integer,
                           primary_key=True, autoincrement=True)
    kinopoisk_id = sqlalchemy.Column(sqlalchemy.Integer, nullable=True)
    festival_id = sqlalchemy.Column(sqlalchemy.Integer, sqlalchemy.ForeignKey("festivals.id"))
    title = sqlalchemy.Column(sqlalchemy.String, nullable=True)

    festival = orm.relation('Festival')
