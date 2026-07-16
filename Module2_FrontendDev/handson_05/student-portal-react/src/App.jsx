import { useState, useEffect } from "react";

import { Footer } from "./components/Footer";
import { Header } from "./components/Header";
import { CourseCard } from "./components/CourseCard";
import { StudentProfile } from "./components/StudentProfile";

export default function App() {

  const [searchTerm, setSearchTerm] = useState("");
  const [enrolledCourses, setEnrolledCourses] = useState([]);
  const [courses, setCourses] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  useEffect(() => {
    let mounted = true;
    fetch("https://jsonplaceholder.typicode.com/posts")
      .then((res) => {
        if (!res.ok) throw new Error("Network response was not ok");
        return res.json();
      })
      .then((data) => {
        if (!mounted) return;
        const first5 = data.slice(0, 5).map((p, idx) => ({
          id: p.id,
          name: p.title.substring(0, 30),
          code: `CS${100 + idx}`,
          credits: 3 + (idx % 2),
          grade: ["A", "B+", "A+", "B", "A"][idx % 5],
        }));
        setCourses(first5);
        setLoading(false);
      })
      .catch((err) => {
        if (!mounted) return;
        setError(err.message || "Failed to fetch");
        setLoading(false);
      });
    return () => {
      mounted = false;
    };
  }, []); 

  useEffect(() => {
    console.log("Courses updated");
  }, [courses]);

  const filteredCourses = courses.filter(
    (course) =>
      course.name.toLowerCase().includes(searchTerm.toLowerCase()) ||
      course.code.toLowerCase().includes(searchTerm.toLowerCase()),
  );

  const handleEnroll = (course) => {
    setEnrolledCourses((prev) =>
      prev.some((enrolled) => enrolled.id === course.id)
        ? prev
        : [...prev, course],
    );
  };

  return (
    <main className="flex flex-col min-h-screen bg-gray-100">
      <Header siteName="Student Portal" />

      <section className="w-full max-w-6xl mx-auto px-4 pt-16 pb-4 flex flex-col sm:flex-row sm:items-center sm:justify-between">
        <div className="mb-4">
          <h2 className="text-2xl font-bold mb-4">Available Courses</h2>
          <input
            value={searchTerm}
            onChange={(e) => setSearchTerm(e.target.value)}
            type="text"
            placeholder="Search courses..."
            className="border border-gray-300 rounded-md py-2 px-4 focus:outline-none focus:ring-2 focus:ring-blue-500"
          />
        </div>
        <div>
          <p className="font-semibold">
            Enrolled Courses: {enrolledCourses.length}
          </p>
        </div>
      </section>

      <div className="w-full max-w-6xl mx-auto px-4 pt-4 pb-16">
        {loading ? (
          <p>Loading...</p>
        ) : error ? (
          <p className="text-red-600">Error: {error}</p>
        ) : (
          <div className="grid gap-4 sm:grid-cols-2 lg:grid-cols-3">
            {filteredCourses.map((course) => (
              <CourseCard
                key={course.id}
                courseId={course.id}
                courseName={course.name}
                courseCode={course.code}
                credits={course.credits}
                grade={course.grade}
                onEnroll={() => handleEnroll(course)}
              />
            ))}
          </div>
        )}
      </div>

      <StudentProfile />

      <Footer />
    </main>
  );
}
