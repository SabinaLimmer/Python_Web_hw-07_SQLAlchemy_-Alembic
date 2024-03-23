from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

engine = create_engine("postgresql://postgres:123123@localhost:5432/postgres")
DBSession = sessionmaker(bind=engine)
session = DBSession()