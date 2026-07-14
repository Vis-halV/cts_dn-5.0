-- Students enrolled in more courses than the average number of courses per student.
SELECT
    s.student_id,
    CONCAT(s.first_name, ' ', s.last_name) AS student_name,
    COUNT(e.course_id) AS total_courses
FROM students s
JOIN enrollments e ON s.student_id = e.student_id
GROUP BY s.student_id, s.first_name, s.last_name
HAVING COUNT(e.course_id) > (
    SELECT AVG(course_count)
    FROM (
        SELECT COUNT(*) AS course_count
        FROM enrollments
        GROUP BY student_id
    ) AS avg_count
);

-- Courses where no student has received an A grade.
SELECT
    c.course_id,
    c.course_name
FROM courses c
WHERE NOT EXISTS (
    SELECT 1
    FROM enrollments e
    WHERE e.course_id = c.course_id
      AND e.grade = 'A'
);

-- Highest paid professor in each department.
SELECT
    p.professor_id,
    p.prof_name,
    p.department_id,
    p.salary
FROM professors p
WHERE p.salary = (
    SELECT MAX(p2.salary)
    FROM professors p2
    WHERE p2.department_id = p.department_id
);

-- Departments with average professor salary greater than 85000.
SELECT *
FROM (
    SELECT
        department_id,
        AVG(salary) AS avg_salary
    FROM professors
    GROUP BY department_id
) AS avg_salary_table
WHERE avg_salary > 85000;

-- Task2: 

CREATE OR REPLACE VIEW vw_student_enrollment_summary AS
SELECT
    s.student_id,
    CONCAT(s.first_name, ' ', s.last_name) AS full_name,
    d.dept_name,
    COUNT(e.course_id) AS total_courses,
    AVG(
        CASE e.grade
            WHEN 'A' THEN 4
            WHEN 'B' THEN 3
            WHEN 'C' THEN 2
            WHEN 'D' THEN 1
            WHEN 'F' THEN 0
        END
    ) AS gpa
FROM students s
JOIN departments d ON s.department_id = d.department_id
LEFT JOIN enrollments e ON s.student_id = e.student_id
GROUP BY s.student_id, s.first_name, s.last_name, d.dept_name;

CREATE OR REPLACE VIEW vw_course_stats AS
SELECT
    c.course_id,
    c.course_name,
    c.course_code,
    COUNT(e.enrollment_id) AS total_enrollments,
    AVG(
        CASE e.grade
            WHEN 'A' THEN 4
            WHEN 'B' THEN 3
            WHEN 'C' THEN 2
            WHEN 'D' THEN 1
            WHEN 'F' THEN 0
        END
    ) AS avg_gpa
FROM courses c
LEFT JOIN enrollments e ON c.course_id = e.course_id
GROUP BY c.course_id, c.course_name, c.course_code;

SELECT *
FROM vw_student_enrollment_summary
WHERE gpa > 3.0;

CREATE OR REPLACE PROCEDURE sp_enroll_student(
    IN p_student_id INT,
    IN p_course_id INT,
    IN p_enrollment_date DATE
)
LANGUAGE plpgsql
AS $$
BEGIN
    IF EXISTS (
        SELECT 1
        FROM enrollments
        WHERE student_id = p_student_id
          AND course_id = p_course_id
    ) THEN
        RAISE EXCEPTION 'Student % is already enrolled in course %', p_student_id, p_course_id;
    END IF;

    INSERT INTO enrollments (student_id, course_id, enrollment_date)
    VALUES (p_student_id, p_course_id, p_enrollment_date);
END;
$$;

CREATE TABLE IF NOT EXISTS department_transfer_log (
    log_id SERIAL PRIMARY KEY,
    student_id INT,
    old_department INT,
    new_department INT,
    transfer_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE OR REPLACE PROCEDURE sp_transfer_student(
    IN p_student INT,
    IN p_new_dept INT
)
LANGUAGE plpgsql
AS $$
DECLARE
    old_dept INT;
BEGIN
    SELECT department_id
    INTO old_dept
    FROM students
    WHERE student_id = p_student;

    IF old_dept IS NULL THEN
        RAISE EXCEPTION 'Student % was not found', p_student;
    END IF;

    UPDATE students
    SET department_id = p_new_dept
    WHERE student_id = p_student;

    INSERT INTO department_transfer_log (student_id, old_department, new_department)
    VALUES (p_student, old_dept, p_new_dept);
END;
$$;
