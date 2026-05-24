from sqlalchemy import Column, String, Integer, Date
from app.database import Base


class Expense(Base):
    __tablename__ = "expenses"
    id = Column(Integer, primary_key=True)
    amount = Column(Integer)
    category = Column(String)
    date = Column(Date)


