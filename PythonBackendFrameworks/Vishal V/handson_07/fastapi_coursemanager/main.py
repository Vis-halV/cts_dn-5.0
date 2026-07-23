from typing import Optional, List

from fastapi import BackgroundTasks, FastAPI, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from database import engine, Base, get_db
import models
from models import 
    Course as CourseModel, 
    Enrollment as EnrollmentModel, 
    Student as StudentModel
from schemas import (
    CourseCreate,
    CourseResponse,
    CourseUpdate,
    EnrollmentCreate,
    EnrollmentResponse,
    StudentCreate,
    StudentResponse,
)

app = FastAPI(
    title='Course Management API',
    description='A REST API built with FastAPI and async SQLAlchemy.',
    version='1.0.0',
    contact={
        'name': 'Course Management API Support',
        'email': 'support@example.com',
    },
)


def send_confirmation_email(student_email: str):
    print(f'Sending confirmation to {student_email}')


@app.on_event('startup')
async def on_startup():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)


@app.get('/')
async def root():
    return {'message': 'API running'}


@app.get('/api/courses/', response_model=List[CourseResponse], tags=['Courses'])
async def get_courses(
    skip: int = 0,
    limit: int = 10,
    department_id: Optional[int] = None,
    db: AsyncSession = Depends(get_db),
):
    query = select(CourseModel)
    if department_id is not None:
        query = query.where(CourseModel.department_id == department_id)
    query = query.offset(skip).limit(limit)

    result = await db.execute(query)
    return result.scalars().all()


@app.post(
    '/api/courses/',
    response_model=CourseResponse,
    status_code=status.HTTP_201_CREATED,
    tags=['Courses'],
    summary='Create a new course',
    response_description='The newly created course',
)
async def create_course(course: CourseCreate, db: AsyncSession = Depends(get_db)):
    new_course = CourseModel(**course.model_dump())
    db.add(new_course)
    await db.commit()
    await db.refresh(new_course)
    return new_course


@app.get('/api/courses/{course_id}', response_model=CourseResponse, tags=['Courses'])
async def get_course(course_id: int, db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(CourseModel).where(CourseModel.id == course_id))
    course = result.scalar_one_or_none()
    if course is None:
        raise HTTPException(status_code=404, detail='Course not found')
    return course


@app.put('/api/courses/{course_id}', response_model=CourseResponse, tags=['Courses'])
async def update_course(course_id: int, course_update: CourseUpdate, db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(CourseModel).where(CourseModel.id == course_id))
    course = result.scalar_one_or_none()
    if course is None:
        raise HTTPException(status_code=404, detail='Course not found')

    update_data = course_update.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(course, field, value)

    await db.commit()
    await db.refresh(course)
    return course


@app.delete('/api/courses/{course_id}', status_code=status.HTTP_204_NO_CONTENT, tags=['Courses'])
async def delete_course(course_id: int, db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(CourseModel).where(CourseModel.id == course_id))
    course = result.scalar_one_or_none()
    if course is None:
        raise HTTPException(status_code=404, detail='Course not found')

    await db.delete(course)
    await db.commit()


@app.get('/api/courses/{course_id}/students/', response_model=List[StudentResponse], tags=['Courses'])
async def get_course_students(course_id: int, db: AsyncSession = Depends(get_db)):
    course_result = await db.execute(select(CourseModel).where(CourseModel.id == course_id))
    if course_result.scalar_one_or_none() is None:
        raise HTTPException(status_code=404, detail='Course not found')

    query = (
        select(StudentModel)
        .join(EnrollmentModel, EnrollmentModel.student_id == StudentModel.id)
        .where(EnrollmentModel.course_id == course_id)
    )
    result = await db.execute(query)
    return result.scalars().all()


@app.get('/api/students/', response_model=List[StudentResponse], tags=['Students'])
async def get_students(db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(StudentModel))
    return result.scalars().all()


@app.post('/api/students/', response_model=StudentResponse, status_code=status.HTTP_201_CREATED, tags=['Students'])
async def create_student(student: StudentCreate, db: AsyncSession = Depends(get_db)):
    new_student = StudentModel(**student.model_dump())
    db.add(new_student)
    await db.commit()
    await db.refresh(new_student)
    return new_student


@app.get('/api/students/{student_id}', response_model=StudentResponse, tags=['Students'])
async def get_student(student_id: int, db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(StudentModel).where(StudentModel.id == student_id))
    student = result.scalar_one_or_none()
    if student is None:
        raise HTTPException(status_code=404, detail='Student not found')
    return student


@app.put('/api/students/{student_id}', response_model=StudentResponse, tags=['Students'])
async def update_student(student_id: int, student_update: StudentCreate, db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(StudentModel).where(StudentModel.id == student_id))
    student = result.scalar_one_or_none()
    if student is None:
        raise HTTPException(status_code=404, detail='Student not found')

    for field, value in student_update.model_dump().items():
        setattr(student, field, value)

    await db.commit()
    await db.refresh(student)
    return student


@app.delete('/api/students/{student_id}', status_code=status.HTTP_204_NO_CONTENT, tags=['Students'])
async def delete_student(student_id: int, db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(StudentModel).where(StudentModel.id == student_id))
    student = result.scalar_one_or_none()
    if student is None:
        raise HTTPException(status_code=404, detail='Student not found')

    await db.delete(student)
    await db.commit()


@app.get('/api/enrollments/', response_model=List[EnrollmentResponse], tags=['Enrollments'])
async def get_enrollments(db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(EnrollmentModel))
    return result.scalars().all()


@app.post(
    '/api/enrollments/',
    response_model=EnrollmentResponse,
    status_code=status.HTTP_201_CREATED,
    tags=['Enrollments'],
)
async def create_enrollment(
    enrollment: EnrollmentCreate,
    background_tasks: BackgroundTasks,
    db: AsyncSession = Depends(get_db),
):
    student_result = await db.execute(select(StudentModel).where(StudentModel.id == enrollment.student_id))
    student = student_result.scalar_one_or_none()
    if student is None:
        raise HTTPException(status_code=404, detail='Student not found')

    course_result = await db.execute(select(CourseModel).where(CourseModel.id == enrollment.course_id))
    if course_result.scalar_one_or_none() is None:
        raise HTTPException(status_code=404, detail='Course not found')

    new_enrollment = EnrollmentModel(**enrollment.model_dump())
    db.add(new_enrollment)
    await db.commit()
    await db.refresh(new_enrollment)

    background_tasks.add_task(send_confirmation_email, student.email)

    return new_enrollment


@app.get('/api/enrollments/{enrollment_id}', response_model=EnrollmentResponse, tags=['Enrollments'])
async def get_enrollment(enrollment_id: int, db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(EnrollmentModel).where(EnrollmentModel.id == enrollment_id))
    enrollment = result.scalar_one_or_none()
    if enrollment is None:
        raise HTTPException(status_code=404, detail='Enrollment not found')
    return enrollment


@app.delete('/api/enrollments/{enrollment_id}', status_code=status.HTTP_204_NO_CONTENT, tags=['Enrollments'])
async def delete_enrollment(enrollment_id: int, db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(EnrollmentModel).where(EnrollmentModel.id == enrollment_id))
    enrollment = result.scalar_one_or_none()
    if enrollment is None:
        raise HTTPException(status_code=404, detail='Enrollment not found')

    await db.delete(enrollment)
    await db.commit()
