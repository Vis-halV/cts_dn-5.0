import React from 'react';
import { useDispatch, useSelector } from 'react-redux';
import { enroll, unenroll } from './enrollmentSlice';

export function CourseList({ courses }) {
  const dispatch = useDispatch();
  const enrolledCourses = useSelector((state) => state.enrollment.enrolledCourses);

  const isEnrolled = (courseId) =>
    enrolledCourses.some((course) => course.id === courseId);

  return (
    <div>
      {courses.map((course) => (
        <div key={course.id}>
          <h3>{course.title}</h3>
          <p>{course.description}</p>
          {isEnrolled(course.id) ? (
            <button onClick={() => dispatch(unenroll(course.id))}>
              Remove
            </button>
          ) : (
            <button onClick={() => dispatch(enroll(course))}>
              Enroll
            </button>
          )}
        </div>
      ))}
    </div>
  );
};

export default CourseList;