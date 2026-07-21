import { useParams, useNavigate } from "react-router-dom";

export function CourseDetailPage() {
  // Implement the useParams hook to get the courseId from the URL
  const { courseId } = useParams();
  const navigate = useNavigate();
  return (
    <div>
      <button
        className="bg-blue-500 text-white px-4 py-2 rounded hover:bg-blue-600"
        onClick={() => {
          navigate("/profile");
        }}
      >
        Enroll
      </button>
      <br />
      <br />
      <h1 className="text-3xl font-bold mb-4">Course Detail Page</h1>
      <p>This is the course detail page for course ID: {courseId}</p>
    </div>
  );
}
