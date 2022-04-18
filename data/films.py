import datetime
import sqlalchemy
from .db_session import SqlAlchemyBase
from sqlalchemy import orm


class Films(SqlAlchemyBase):
    __tablename__ = 'films'

    id = sqlalchemy.Column(sqlalchemy.Integer,
                           primary_key=True, autoincrement=True)
    user_id = sqlalchemy.Column(sqlalchemy.Integer, sqlalchemy.ForeignKey("users.id"))
    kinopoisk_id = sqlalchemy.Column(sqlalchemy.Integer, nullable=True)
    festival_id = sqlalchemy.Column(sqlalchemy.Integer, nullable=True)  # доделать когда появится таблица с фестивалями
    title = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    is_approved = sqlalchemy.Column(sqlalchemy.Boolean, nullable=True)
    # festival = orm.relation('Festival')
    user = orm.relation('User')
