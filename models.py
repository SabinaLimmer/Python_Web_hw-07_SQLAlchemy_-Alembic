from datetime import datetime

from sqlalchemy import Column, Integer, String, Boolean
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from sqlalchemy.sql.schema import ForeignKey, Table
from sqlalchemy.sql.sqltypes import DateTime

from db_session import engine

Base = declarative_base()


class Group(Base):
    __tablename__ = 'groups'

    id = Column(Integer, primary_key=True)
    group_number = Column(Integer, nullable=False)
    students = relationship("Student", back_populates="group")

class Student(Base):
    __tablename__ = 'students'

    id = Column(Integer, primary_key=True)
    student_name = Column(String(100), nullable=False)
    group_id = Column(Integer, ForeignKey('groups.id', ondelete='CASCADE'))

    group = relationship("Group", back_populates="students")
    grades = relationship("Grade", back_populates="student")

class Lecturer(Base):
    __tablename__ = 'lecturers'

    id = Column(Integer, primary_key=True)
    lecturer_name = Column(String(100), nullable=False)
    subjects_taught = relationship("Subject", back_populates="lecturer")

class Subject(Base):
    __tablename__ = 'subjects'

    id = Column(Integer, primary_key=True)
    subject_name = Column(String(30), nullable=False)
    lecturer_id = Column(Integer, ForeignKey('lecturers.id', ondelete='CASCADE'))

    lecturer = relationship("Lecturer", back_populates="subjects_taught")
    grades = relationship("Grade", back_populates="subject")

class Grade(Base):
    __tablename__ = 'grades'

    id = Column(Integer, primary_key=True)
    grade = Column(Integer, nullable=False)
    date_of = Column(DateTime, default=datetime.now())
    student_id = Column(Integer, ForeignKey('students.id', ondelete='CASCADE'))
    subject_id = Column(Integer, ForeignKey('subjects.id', ondelete='CASCADE'))

    student = relationship("Student", back_populates="grades")
    subject = relationship("Subject", back_populates="grades")


Base.metadata.create_all(engine)

