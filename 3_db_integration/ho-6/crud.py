from datetime import date
from sqlalchemy.orm import sessionmaker, joinedload
from models import engine, Department, Student, Course, Enrollment, Professor

Session = sessionmaker(bind=engine)
session = Session()

def insert_departments_and_students():
    print("\n--- Inserting Departments and Students ---")

    dept_cs   = Department(dept_name="Computer Science", head_of_dept="Dr. Ramesh Kumar", budget=850000.00)
    dept_ec   = Department(dept_name="Electronics",      head_of_dept="Dr. Priya Nair",   budget=620000.00)
    dept_mech = Department(dept_name="Mechanical",       head_of_dept="Dr. Suresh Iyer",  budget=540000.00)

    session.add_all([dept_cs, dept_ec, dept_mech])
    session.flush()   

    students = [
        Student(first_name="Arjun",  last_name="Mehta",  email="arjun.mehta@college.edu",  date_of_birth=date(2003,4,12),  department_id=dept_cs.department_id,   enrollment_year=2022),
        Student(first_name="Priya",  last_name="Suresh", email="priya.suresh@college.edu", date_of_birth=date(2003,7,25),  department_id=dept_cs.department_id,   enrollment_year=2022),
        Student(first_name="Rohan",  last_name="Verma",  email="rohan.verma@college.edu",  date_of_birth=date(2002,11,8),  department_id=dept_ec.department_id,   enrollment_year=2021),
        Student(first_name="Sneha",  last_name="Patel",  email="sneha.patel@college.edu",  date_of_birth=date(2004,1,30),  department_id=dept_mech.department_id, enrollment_year=2023),
        Student(first_name="Vikram", last_name="Das",    email="vikram.das@college.edu",   date_of_birth=date(2003,9,14),  department_id=dept_cs.department_id,   enrollment_year=2022),
    ]

    session.add_all(students)
    session.commit()
    print(f"Inserted {len(students)} students across 3 departments.")

def insert_courses_and_enrollments():
    print("\n--- Inserting Courses and Enrollments ---")

    dept_cs   = session.query(Department).filter_by(dept_name="Computer Science").first()
    dept_ec   = session.query(Department).filter_by(dept_name="Electronics").first()
    dept_mech = session.query(Department).filter_by(dept_name="Mechanical").first()

    courses = [
        Course(course_name="Data Structures & Algorithms", course_code="CS101", credits=4, department_id=dept_cs.department_id),
        Course(course_name="Circuit Theory",               course_code="EC101", credits=3, department_id=dept_ec.department_id),
        Course(course_name="Thermodynamics",               course_code="ME101", credits=3, department_id=dept_mech.department_id),
    ]
    session.add_all(courses)
    session.flush()

    arjun  = session.query(Student).filter_by(email="arjun.mehta@college.edu").first()
    priya  = session.query(Student).filter_by(email="priya.suresh@college.edu").first()
    rohan  = session.query(Student).filter_by(email="rohan.verma@college.edu").first()
    vikram = session.query(Student).filter_by(email="vikram.das@college.edu").first()
    cs101  = session.query(Course).filter_by(course_code="CS101").first()
    ec101  = session.query(Course).filter_by(course_code="EC101").first()
    me101  = session.query(Course).filter_by(course_code="ME101").first()

    enrollments = [
        Enrollment(student_id=arjun.student_id,  course_id=cs101.course_id, enrollment_date=date(2022,9,1), grade="A"),
        Enrollment(student_id=priya.student_id,  course_id=cs101.course_id, enrollment_date=date(2022,9,1), grade="B"),
        Enrollment(student_id=rohan.student_id,  course_id=ec101.course_id, enrollment_date=date(2021,9,1), grade="A"),
        Enrollment(student_id=vikram.student_id, course_id=me101.course_id, enrollment_date=date(2022,9,1), grade="B"),
    ]
    session.add_all(enrollments)
    session.commit()
    print(f"Inserted {len(courses)} courses and {len(enrollments)} enrollments.")

def read_cs_students():
    print("\n--- Students in Computer Science ---")

    students = (
        session.query(Student)
        .join(Department)
        .filter(Department.dept_name == "Computer Science")
        .all()
    )

    for s in students:
        print(f"  {s.student_id}: {s.first_name} {s.last_name} | year: {s.enrollment_year}")

def read_enrollments_n_plus_1():
    print("\n--- Enrollments (N+1 — watch SQL log) ---")

    enrollments = session.query(Enrollment).all()

    for e in enrollments:
        print(f"  {e.student.first_name} {e.student.last_name} → {e.course.course_name} | grade: {e.grade}")

def update_student_year():
    print("\n--- Update enrollment_year for Priya Suresh ---")

    student = session.query(Student).filter_by(email="priya.suresh@college.edu").first()

    if student:
        print(f"  Before: {student.first_name} — year {student.enrollment_year}")
        student.enrollment_year = 2023
        session.commit()
        print(f"  After:  {student.first_name} — year {student.enrollment_year}")
    else:
        print("  Student not found.")
        
def delete_enrollment():
    print("\n--- Delete Vikram's ME101 enrollment ---")

    vikram = session.query(Student).filter_by(email="vikram.das@college.edu").first()
    me101  = session.query(Course).filter_by(course_code="ME101").first()

    enrollment = session.query(Enrollment).filter_by(
        student_id=vikram.student_id,
        course_id=me101.course_id
    ).first()

    if enrollment:
        session.delete(enrollment)
        session.commit()
        print(f"  Deleted enrollment: student {vikram.first_name} from {me101.course_code}")
    else:
        print("  Enrollment not found.")

    # Verify
    remaining = session.query(Enrollment).count()
    print(f"  Remaining enrollments: {remaining}")
    
def read_enrollments_joinedload():
    print("\n--- Enrollments with joinedload (N+1 FIXED) ---")

    enrollments = (
        session.query(Enrollment)
        .options(
            joinedload(Enrollment.student),   
            joinedload(Enrollment.course)     
        )
        .all()
    )

    for e in enrollments:
        print(f"  {e.student.first_name} {e.student.last_name} → {e.course.course_name} | grade: {e.grade}")

    print("  With joinedload you should see exactly 1 SELECT with LEFT OUTER JOINs.")
    
if __name__ == "__main__":
    insert_departments_and_students()   
    insert_courses_and_enrollments()    
    read_cs_students()                  
    read_enrollments_n_plus_1()         
    update_student_year()               
    delete_enrollment()                 
    read_enrollments_joinedload()        