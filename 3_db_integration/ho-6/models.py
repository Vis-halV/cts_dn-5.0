
from sqlalchemy import (
    create_engine, Column, Integer, String,
    ForeignKey, Date, Numeric, CheckConstraint
)
from sqlalchemy.orm import relationship, declarative_base 

DATABASE_URL = "postgresql+psycopg2://postgres:9833@localhost:5432/college_db_orm"

engine = create_engine(
    DATABASE_URL,
    echo=True   
)

Base = declarative_base()


class Department(Base):
    __tablename__ = "departments"

    department_id = Column(Integer, primary_key=True, autoincrement=True)
    dept_name     = Column(String(20), nullable=False)
    head_of_dept  = Column(String(20))
    budget        = Column(Numeric(8, 2))

    students     = relationship("Student",    back_populates="department")
    courses      = relationship("Course",     back_populates="department")
    professors   = relationship("Professor",  back_populates="department")

    def __repr__(self):
        return f"<Department(id={self.department_id}, name='{self.dept_name}')>"


class Student(Base):
    __tablename__ = "students"

    student_id      = Column(Integer, primary_key=True, autoincrement=True)
    first_name      = Column(String(16), nullable=False)
    last_name       = Column(String(16), nullable=False)
    email           = Column(String(32), unique=True, nullable=False)
    date_of_birth   = Column(Date)
    department_id   = Column(Integer, ForeignKey("departments.department_id"))
    enrollment_year = Column(Integer)

    department  = relationship("Department", back_populates="students")
    enrollments = relationship("Enrollment", back_populates="student")

    def __repr__(self):
        return f"<Student(id={self.student_id}, name='{self.first_name} {self.last_name}')>"


class Course(Base):
    __tablename__ = "courses"

    course_id     = Column(Integer, primary_key=True, autoincrement=True)
    course_name   = Column(String(32), nullable=False)
    course_code   = Column(String(8),  unique=True)
    credits       = Column(Integer)
    department_id = Column(Integer, ForeignKey("departments.department_id"))
    max_seats     = Column(Integer, default=60)

    department  = relationship("Department", back_populates="courses")
    enrollments = relationship("Enrollment", back_populates="course")

    def __repr__(self):
        return f"<Course(id={self.course_id}, code='{self.course_code}')>"


class Enrollment(Base):
    __tablename__ = "enrollments"

    enrollment_id   = Column(Integer, primary_key=True, autoincrement=True)
    student_id      = Column(Integer, ForeignKey("students.student_id"))
    course_id       = Column(Integer, ForeignKey("courses.course_id"))
    enrollment_date = Column(Date)
    grade           = Column(String(1), CheckConstraint("grade IN ('A','B','C','D','F')"))

    student = relationship("Student", back_populates="enrollments")
    course  = relationship("Course",  back_populates="enrollments")

    def __repr__(self):
        return f"<Enrollment(student_id={self.student_id}, course_id={self.course_id}, grade='{self.grade}')>"


class Professor(Base):
    __tablename__ = "professors"

    professor_id  = Column(Integer, primary_key=True, autoincrement=True)
    prof_name     = Column(String(24), nullable=False)
    email         = Column(String(32), unique=True)
    department_id = Column(Integer, ForeignKey("departments.department_id"))
    salary        = Column(Numeric(8, 2))

    department = relationship("Department", back_populates="professors")

    def __repr__(self):
        return f"<Professor(id={self.professor_id}, name='{self.prof_name}')>"

if __name__ == "__main__":
    print("Creating tables in college_db_orm ...")
    Base.metadata.create_all(engine)
    print("Done. Connect with psql and run \\dt to verify.")