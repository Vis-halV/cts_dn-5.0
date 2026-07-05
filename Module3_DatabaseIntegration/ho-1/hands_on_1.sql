-- TASK 1: CREATE THE DATABASE AND TABLES

-- STEP 1: Create and connect to the database
  createdb college_db
  \c college_db

-- STEP 2A: Create the departments table FIRST
CREATE TABLE departments (
    department_id SERIAL PRIMARY KEY,
    dept_name     VARCHAR(20) NOT NULL,
    hod_name      VARCHAR(20),
    budget        DECIMAL(8,2)
);

-- STEP 2B: Create the students table
CREATE TABLE students (
    student_id      SERIAL PRIMARY KEY,
    first_name      VARCHAR(16) NOT NULL,
    last_name       VARCHAR(16) NOT NULL,
    email           VARCHAR(32) UNIQUE NOT NULL,
    date_of_birth   DATE,
    department_id   INT,
    enrollment_year INT,

    FOREIGN KEY (department_id)
        REFERENCES departments(department_id)
);

-- STEP 2C: Create the courses table
CREATE TABLE courses (
    course_id     SERIAL PRIMARY KEY,
    course_name   VARCHAR(32) NOT NULL,
    course_code   VARCHAR(8) UNIQUE,
    credits       INT,
    department_id INT,

    FOREIGN KEY (department_id)
        REFERENCES departments(department_id)
);

-- STEP 2D: Create the enrollments table
CREATE TABLE enrollments (
    enrollment_id   SERIAL PRIMARY KEY,
    student_id      INT,
    course_id       INT,
    enrollment_date DATE,
    grade           CHAR(3),

    FOREIGN KEY (student_id)
        REFERENCES students(student_id),

    FOREIGN KEY (course_id)
        REFERENCES courses(course_id)
);

-- STEP 2E: Create the professors table
CREATE TABLE professors (
    professor_id  SERIAL PRIMARY KEY,
    prof_name     VARCHAR(24) NOT NULL,
    email         VARCHAR(32) UNIQUE,
    department_id INT,
    salary        DECIMAL(8,2),

    FOREIGN KEY (department_id)
        REFERENCES departments(department_id)
);

-- STEP 3: Verify all tables were created
-- Run these in psql to confirm:
--   \dt                    — lists all tables
--   \d departments         — describes columns + constraints
--   \d students
--   \d courses
--   \d enrollments
--   \d professors

-- TASK 2: VERIFY NORMALISATION

-- 1NF — First Normal Form
-- Rule: Every column must hold a single, atomic value.
--       No repeating groups or comma-separated lists.
--
-- Status: SATISFIED
-- Every column in all five tables stores one value per row.

-- 2NF — Second Normal Form
-- Rule: Every non-key column must depend on the WHOLE primary key.
--       Only relevant when the primary key is composite.
--
-- Status: SATISFIED

-- 3NF — Third Normal Form
-- Rule: No transitive dependencies.
--       Non-key column A must not depend on non-key column B
--       which depends on the primary key.
--
-- Status: SATISFIED across all tables.

-- TASK 3: ALTER AND EXTEND THE SCHEMA

-- STEP 10: Add phone_number column to students
ALTER TABLE students
    ADD COLUMN phone_number VARCHAR(15);

-- STEP 11: Add max_seats column to courses with default value
ALTER TABLE courses
    ADD COLUMN max_seats INT DEFAULT 60;

-- STEP 12: Add CHECK constraint on grade in enrollments
-- Allowed values: A, B, C, D, F — or NULL
ALTER TABLE enrollments
    ADD CONSTRAINT chk_grade
    CHECK (grade IN ('A', 'B', 'C', 'D', 'F') OR grade IS NULL);

-- STEP 13: Rename hod_name → head_of_dept in departments
ALTER TABLE departments
    RENAME COLUMN hod_name TO head_of_dept;

-- STEP 14: Drop phone_number from students (schema rollback)
-- Simulates reverting step 10 without data loss to other columns
ALTER TABLE students
    DROP COLUMN phone_number;

-- Verify
-- \d departments    — head_of_dept (renamed), no hod_name
-- \d students       — no phone_number (dropped)
-- \d courses        — max_seats INT DEFAULT 60 present
-- \d enrollments    — chk_grade CHECK constraint present
-- \d professors     — unchanged from creation
