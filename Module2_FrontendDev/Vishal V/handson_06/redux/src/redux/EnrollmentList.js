import React from 'react';
import { useSelector, useDispatch } from 'react-redux';
import { unenroll } from './enrollmentSlice';

export default function EnrollmentList() {
  const dispatch = useDispatch();
  const enrolledCourses = useSelector((state) => state.enrollment.enrolledCourses);

  return (
    <div>
      <h2>Enrolled Courses</h2>
      {enrolledCourses.length === 0 ? (
        <p>No courses enrolled yet.</p>
      ) : (
        enrolledCourses.map((course) => (
          <div key={course.id}>
            <span>{course.title}</span>
            <button onClick={() => dispatch(unenroll(course.id))}>Remove</button>
          </div>
        ))
      )}
    </div>
  );
};
