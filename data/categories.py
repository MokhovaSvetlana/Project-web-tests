import sqlalchemy
from data.db_session import SqlAlchemyBase


association_table = sqlalchemy.Table(
    'Categories_to_Tests',
    SqlAlchemyBase.metadata,
    sqlalchemy.Column('categories', sqlalchemy.Integer,
                      sqlalchemy.ForeignKey('tests.id')),
    sqlalchemy.Column('tests', sqlalchemy.Integer,
                      sqlalchemy.ForeignKey('categories.id'))
)

association2_table = sqlalchemy.Table(
    'Categories_to_Offered_Tests',
    SqlAlchemyBase.metadata,
    sqlalchemy.Column('categories', sqlalchemy.Integer,
                      sqlalchemy.ForeignKey('offered_tests.id')),
    sqlalchemy.Column('offered_tests', sqlalchemy.Integer,
                      sqlalchemy.ForeignKey('categories.id'))
)


class Category(SqlAlchemyBase):

    __tablename__ = 'categories'
    id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True, autoincrement=True)
    name = sqlalchemy.Column(sqlalchemy.String, unique=False, nullable=False)
