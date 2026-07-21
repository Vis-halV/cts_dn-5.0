import { useContext } from 'react';
import { EnrollmentContext } from '../context/EnrollmentContext';

export function ProfilePage() {
  const { enrolledCourses, removeCourse } = useContext(EnrollmentContext);

  return (
    <div className="flex flex-col items-center justify-center min-h-screen py-2">
      <h2 className="text-2xl font-bold mb-4">My Courses</h2>
      {enrolledCourses.length === 0 ? (
        <p>No courses enrolled yet.</p>
      ) : (
        <ul className="list-disc list-inside">
          {enrolledCourses.map((course) => (
            <li key={course.id} className="mb-2">
              {course.title}{' '}
              <button onClick={() => removeCourse(course.id)} className="bg-red-500 text-white px-4 py-2 rounded hover:bg-red-600">
                Un-enroll
              </button>
            </li>
          ))}
        </ul>
      )}
    </div>
  );
}
