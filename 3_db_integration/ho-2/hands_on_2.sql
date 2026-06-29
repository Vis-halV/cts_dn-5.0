-- Task 1: Insert, Update and Delete Data
-- STEP 15: Insert sample data into all five tables

INSERT INTO departments (dept_name, head_of_dept, budget) VALUES
    ('Computer Science', 'Dr. Smith',    750000.00),
    ('Mathematics',      'Dr. Johnson',  500000.00),
    ('Physics',          'Dr. Williams', 620000.00),
    ('English',          'Dr. Brown',    480000.00);

-- Verify
SELECT * FROM departments;


-- Students
INSERT INTO students (first_name, last_name, email, date_of_birth, department_id, enrollment_year) VALUES
    ('Alice',   'Martin',   'alice.martin@college.edu',   '2001-03-15', 1, 2021),
    ('Bob',     'Harris',   'bob.harris@college.edu',     '2000-07-22', 2, 2020),
    ('Carol',   'White',    'carol.white@college.edu',    '2002-11-05', 1, 2022),
    ('David',   'Clark',    'david.clark@college.edu',    '2001-01-30', 3, 2021),
    ('Eva',     'Lewis',    'eva.lewis@college.edu',      '2003-06-18', 2, 2022),
    ('Frank',   'Walker',   'frank.walker@college.edu',   '2000-09-12', 4, 2020),
    ('Grace',   'Hall',     'grace.hall@college.edu',     '2002-04-25', 3, 2022),
    ('Henry',   'Allen',    'henry.allen@college.edu',    '2001-12-08', 1, 2021);

-- Verify
SELECT COUNT(*) FROM students;


-- Courses
INSERT INTO courses (course_name, course_code, credits, department_id) VALUES
    ('Introduction to Programming', 'CS101', 4, 1),
    ('Data Structures',             'CS201', 4, 1),
    ('Calculus I',                  'MA101', 3, 2),
    ('Linear Algebra',              'MA201', 3, 2),
    ('Classical Mechanics',         'PH101', 3, 3);

-- Verify
SELECT * FROM courses;


-- Professors
INSERT INTO professors (prof_name, email, department_id, salary) VALUES
    ('Dr. Adams',   'adams@college.edu',   1, 95000.00),
    ('Dr. Baker',   'baker@college.edu',   2, 88000.00),
    ('Dr. Carter',  'carter@college.edu',  3, 82000.00),
    ('Dr. Davis',   'davis@college.edu',   4, 79000.00),
    ('Dr. Evans',   'evans@college.edu',   1, 91000.00),
    ('Dr. Foster',  'foster@college.edu',  2, 85000.00);

-- Verify
SELECT * FROM professors;


-- Enrollments
INSERT INTO enrollments (student_id, course_id, enrollment_date, grade) VALUES
    (1, 1, '2021-09-01', 'A'),
    (1, 2, '2021-09-01', 'B'),
    (2, 3, '2020-09-01', 'A'),
    (2, 4, '2020-09-01', 'B'),
    (3, 1, '2022-09-01', 'C'),
    (4, 5, '2021-09-01', 'B'),
    (5, 3, '2022-09-01', 'A'),
    (6, 1, '2020-09-01', 'B'),
    (7, 5, '2022-09-01', NULL),
    (8, 2, '2021-09-01', NULL);

-- Verify
SELECT * FROM enrollments;


-- STEP 16: Insert two additional students of your own choosing
INSERT INTO students (first_name, last_name, email, date_of_birth, department_id, enrollment_year) VALUES
    ('Irene',  'Scott',   'irene.scott@college.edu',  '2002-08-14', 2, 2022),
    ('James',  'Morgan',  'james.morgan@college.edu', '2001-05-20', 4, 2021);

SELECT * FROM students;

-- STEP 17: Update grade for student_id = 5, course_id = 1
-- Change grade from 'C' → 'B'
-- Preview first, then update

-- Preview
SELECT * FROM enrollments
WHERE student_id = 11 AND course_id = 1;

-- Update
UPDATE enrollments
SET    grade = 'B'
WHERE  student_id = 11
AND    course_id  = 1;

-- Verify
SELECT * FROM enrollments
WHERE student_id = 11 AND course_id = 1;

-- STEP 18: Delete enrollments where grade IS NULL
-- Delete
DELETE FROM enrollments
WHERE grade IS NULL;

-- STEP 19: Verify row counts after all DML operations
SELECT 'departments' AS table_name, COUNT(*) AS row_count FROM departments
UNION ALL
SELECT 'students',   COUNT(*) FROM students
UNION ALL
SELECT 'courses',    COUNT(*) FROM courses
UNION ALL
SELECT 'professors', COUNT(*) FROM professors
UNION ALL
SELECT 'enrollments',COUNT(*) FROM enrollments;


-- TASK 2: SINGLE-TABLE QUERIES AND FILTERING

-- STEP 20: All students enrolled in 2022, ordered by last_name
SELECT student_id,
       first_name,
       last_name,
       email,
       enrollment_year
FROM   students
WHERE  enrollment_year = 2022
ORDER  BY last_name ASC;


-- STEP 21: All courses with more than 3 credits, sorted by
--          credits descending
SELECT course_id,
       course_name,
       course_code,
       credits
FROM   courses
WHERE  credits > 3
ORDER  BY credits DESC;

-- STEP 22: Professors with salary between 80,000 and 95,000
-- BETWEEN is inclusive on both ends
SELECT professor_id,
       prof_name,
       email,
       salary
FROM   professors
WHERE  salary BETWEEN 80000 AND 95000
ORDER  BY salary DESC;

-- STEP 23: Students whose email ends with '@college.edu'
-- % wildcard matches any sequence of characters before the domain
SELECT student_id,
       first_name,
       last_name,
       email
FROM   students
WHERE  email LIKE '%@college.edu';

-- STEP 24: Count of students per enrollment_year
-- Expected: 3 rows — one per distinct year (2020, 2021, 2022)
SELECT enrollment_year,
       COUNT(*) AS student_count
FROM   students
GROUP  BY enrollment_year
ORDER  BY enrollment_year ASC;

-- TASK 3: MULTI-TABLE JOINS

-- STEP 25: Each student's full name alongside their department
-- Tables: students JOIN departments
SELECT s.student_id,
       s.first_name || ' ' || s.last_name AS full_name,
       d.dept_name
FROM   students    s
JOIN   departments d ON s.department_id = d.department_id
ORDER  BY s.last_name ASC;


-- STEP 26: Each enrollment with student name and course name
-- Tables: enrollments JOIN students JOIN courses (3-table JOIN)
SELECT e.enrollment_id,
       s.first_name || ' ' || s.last_name AS student_name,
       c.course_name,
       e.enrollment_date,
       e.grade
FROM   enrollments e
JOIN   students    s ON e.student_id = s.student_id
JOIN   courses     c ON e.course_id  = c.course_id
ORDER  BY e.enrollment_id ASC;


-- STEP 27: Students NOT enrolled in any course
-- Pattern: LEFT JOIN + WHERE right-side key IS NULL
-- Students with no matching row in enrollments will show NULL
SELECT s.student_id,
       s.first_name || ' ' || s.last_name AS full_name,
       s.email
FROM   students    s
LEFT   JOIN enrollments e ON s.student_id = e.student_id
WHERE  e.student_id IS NULL;


-- STEP 28: Every course with its enrollment count
-- Courses with zero enrollments must still appear → LEFT JOIN
SELECT c.course_id,
       c.course_name,
       c.course_code,
       COUNT(e.enrollment_id) AS enrollment_count
FROM   courses     c
LEFT   JOIN enrollments e ON c.course_id = e.course_id
GROUP  BY c.course_id, c.course_name, c.course_code
ORDER  BY enrollment_count DESC;


-- STEP 29: Each department with its professors and salaries
-- Include departments with no professors yet → LEFT JOIN
SELECT d.dept_name,
       p.prof_name,
       p.salary
FROM   departments d
LEFT   JOIN professors p ON d.department_id = p.department_id
ORDER  BY d.dept_name ASC, p.salary DESC NULLS LAST;


-- TASK 4: AGGREGATIONS AND GROUPING

-- STEP 30: Total enrollments per course
-- Display course_name and enrollment_count
SELECT c.course_name,
       COUNT(e.enrollment_id) AS enrollment_count
FROM   courses     c
LEFT   JOIN enrollments e ON c.course_id = e.course_id
GROUP  BY c.course_id, c.course_name
ORDER  BY enrollment_count DESC;

-- STEP 31: Average professor salary per department
-- Rounded to 2 decimal places
-- Expected: 4 rows — one per department
SELECT d.dept_name,
       ROUND(AVG(p.salary), 2) AS avg_salary
FROM   departments d
JOIN   professors  p ON d.department_id = p.department_id
GROUP  BY d.department_id, d.dept_name
ORDER  BY avg_salary DESC;

-- STEP 32: Departments where total budget exceeds 600,000
SELECT dept_name,
       budget
FROM   departments
WHERE  budget > 600000
ORDER  BY budget DESC;

-- STEP 33: Grade distribution for course CS101
-- Count of each grade value
SELECT e.grade,
       COUNT(*) AS grade_count
FROM   enrollments e
JOIN   courses     c ON e.course_id = c.course_id
WHERE  c.course_code = 'CS101'
GROUP  BY e.grade
ORDER  BY e.grade ASC;

-- STEP 34: Departments where more than 2 students are enrolled
-- Use HAVING to filter on the aggregated count, not WHERE
SELECT d.dept_name,
       COUNT(DISTINCT e.student_id) AS enrolled_students
FROM   departments  d
JOIN   courses      c ON d.department_id = c.department_id
JOIN   enrollments  e ON c.course_id     = e.course_id
GROUP  BY d.department_id, d.dept_name
HAVING COUNT(DISTINCT e.student_id) > 2
ORDER  BY enrolled_students DESC;
