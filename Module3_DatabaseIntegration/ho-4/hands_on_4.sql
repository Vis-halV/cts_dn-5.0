-- Check the execution plan before adding indexes.
EXPLAIN ANALYZE
SELECT
    s.first_name,
    s.last_name,
    c.course_name
FROM enrollments e
JOIN students s ON s.student_id = e.student_id
JOIN courses c ON c.course_id = e.course_id
WHERE s.enrollment_year = 2022;

-- Indexes used by the join/filter workload.
CREATE INDEX IF NOT EXISTS idx_students_enrollment_year
ON students (enrollment_year);

CREATE UNIQUE INDEX IF NOT EXISTS idx_student_course
ON enrollments (student_id, course_id);

CREATE INDEX IF NOT EXISTS idx_course_code
ON courses (course_code);

-- Run the plan again after indexing and compare cost/time.
EXPLAIN ANALYZE
SELECT
    s.first_name,
    s.last_name,
    c.course_name
FROM enrollments e
JOIN students s ON s.student_id = e.student_id
JOIN courses c ON c.course_id = e.course_id
WHERE s.enrollment_year = 2022;

