import datetime
import sqlalchemy
from .db_session import SqlAlchemyBase
from sqlalchemy import orm


class Festival(SqlAlchemyBase):
    __tablename__ = 'festivals'

    id = sqlalchemy.Column(sqlalchemy.Integer,
                           primary_key=True, autoincrement=True)
    title = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    description = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    genres = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    start_date = sqlalchemy.Column(sqlalchemy.Date, nullable=True)
    end_date = sqlalchemy.Column(sqlalchemy.Date, nullable=True)

    # film = orm.relation('Films', back_populates='festival')