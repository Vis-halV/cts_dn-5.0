import { useEffect } from "react";
import { useDispatch, useSelector } from "react-redux";
import {
  fetchAllCourses,
  selectCourses,
  selectCoursesLoading,
  selectCoursesError,
} from "../store/coursesSlice";

export default function CoursesPage() {
  const dispatch = useDispatch();
  const courses = useSelector(selectCourses);
  const loading = useSelector(selectCoursesLoading);
  const error = useSelector(selectCoursesError);

  useEffect(() => {
    dispatch(fetchAllCourses());
  }, [dispatch]);

  if (loading) {
    return <p className="text-center text-gray-500 py-8">Loading courses…</p>;
  }

  if (error) {
    return (
      <div className="bg-red-50 border border-red-300 text-red-700 rounded-lg p-4 m-4">
        {error}
      </div>
    );
  }

  return (
    <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-4 p-6">
      {courses.map((course) => (
        <div
          key={course.id}
          className="bg-white shadow-md rounded-xl p-4 border border-gray-100 hover:shadow-lg transition-shadow"
        >
          <h3 className="text-lg font-semibold text-gray-800">{course.title}</h3>
          <p className="text-sm text-gray-500 mt-1">{course.description}</p>
        </div>
      ))}
    </div>
  );
}
