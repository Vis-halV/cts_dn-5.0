import { createContext, useState } from 'react';

export const EnrollmentContext = createContext();

export function EnrollmentProvider({ children }) {
  const [enrolledCourses, setEnrolledCourses] = useState([]);

  const enrollCourse = (course) => {
    setEnrolledCourses((prevCourses) => {
      if (prevCourses.some((c) => c.id === course.id)) {
        return prevCourses;
      }
      return [...prevCourses, course];
    });
  };

  const removeCourse = (courseId) => {
    setEnrolledCourses((prevCourses) => prevCourses.filter((c) => c.id !== courseId));
  };

  return (
    <EnrollmentContext.Provider value={{ enrolledCourses, enrollCourse, removeCourse }}>
      {children}
    </EnrollmentContext.Provider>
  );
}
