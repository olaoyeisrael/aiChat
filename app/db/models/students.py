from sqlalchemy import Column, Integer, String
from app.core.database import Base

class Student(Base):
    __tablename__ = "students"
    id = Column(Integer, primary_key=True, index=True)
    registration_no = Column(String, unique=True, index=True)
    password = Column(String(250))
    role = Column(String, default="student", nullable=False)