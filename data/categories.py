import sqlalchemy
from data.db import Base


association_table = sqlalchemy.Table(
    'Categories_to_Tests',
    Base.metadata,
    sqlalchemy.Column('categories', sqlalchemy.Integer,
                      sqlalchemy.ForeignKey('tests.id')),
    sqlalchemy.Column('tests', sqlalchemy.Integer,
                      sqlalchemy.ForeignKey('categories.id'))
)

association2_table = sqlalchemy.Table(
    'Categories_to_Offered_Tests',
    Base.metadata,
    sqlalchemy.Column('categories', sqlalchemy.Integer,
                      sqlalchemy.ForeignKey('offered_tests.id')),
    sqlalchemy.Column('offered_tests', sqlalchemy.Integer,
                      sqlalchemy.ForeignKey('categories.id'))
)


class Category(Base):

    __tablename__ = 'categories'
    id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True, autoincrement=True)
    name = sqlalchemy.Column(sqlalchemy.String, unique=False, nullable=False)
