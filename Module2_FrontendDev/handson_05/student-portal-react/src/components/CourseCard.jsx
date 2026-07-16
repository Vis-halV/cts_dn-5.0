export function CourseCard({
  courseId,
  courseName,
  courseCode,
  credits,
  grade,
  onEnroll,
}) {
  return (
    <div className="bg-white border border-gray-200 shadow-lg rounded-xl overflow-hidden p-6 max-w-sm w-full">
      <div className="space-y-1 text-gray-600" id={`course-${courseId}`}>
        <p>Course ID: {courseId}</p>
        <p>Course Name: {courseName}</p>
        <p>Course Code: {courseCode}</p>
        <p>Credits: {credits}</p>
        <p>Grade: {grade}</p>

        <button
          onClick={onEnroll}
          className="mt-4 bg-blue-600 text-white px-4 py-2 rounded-lg hover:bg-blue-700 transition"
        >
          Enroll
        </button>
      </div>
    </div>
  );
}
