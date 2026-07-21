import { useContext } from 'react';
import { EnrollmentContext } from '../context/EnrollmentContext';

const courses = [
  { id: 'c1', title: 'React Basics' },
  { id: 'c2', title: 'Advanced JavaScript' },
  { id: 'c3', title: 'Web Accessibility' },
];

export function CoursesPage() {
  const { enrollCourse, enrolledCourses } = useContext(EnrollmentContext);

  return (
    <div className="flex flex-col items-center justify-center min-h-screen py-2">
      <h2 className="text-2xl font-bold mb-4">Courses</h2>
      <ul className="list-disc list-inside">
        {courses.map((course) => {
          const isEnrolled = enrolledCourses.some((c) => c.id === course.id);
          return (
            <li key={course.id} className="mb-2">
              {course.title}{' '}
              <button onClick={() => enrollCourse(course)} disabled={isEnrolled} className="bg-blue-500 text-white px-4 py-2 rounded hover:bg-blue-600">
                {isEnrolled ? 'Enrolled' : 'Enroll'}
              </button>
            </li>
          );
        })}
      </ul>
    </div>
  );
}
