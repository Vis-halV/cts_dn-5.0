Step 1 

Note the current head revision

```bash
alembic current
```

~\OneDrive\Desktop\CTS\git-local\cts_dn-5.0\3_db_integration\ho-7> alembic current
INFO  [alembic.runtime.migration] Context impl PostgresqlImpl.
INFO  [alembic.runtime.migration] Will assume transactional DDL.
dd75a2adc1fa (head)
~\OneDrive\Desktop\CTS\git-local\cts_dn-5.0\3_db_integration\ho-7> 

```copy 
dd75a2adc1fa
```

Step 2 

Rollback and drop course_schedules table

```bash
alembic downgrade -1
```

~\OneDrive\Desktop\CTS\git-local\cts_dn-5.0\3_db_integration\ho-7> alembic downgrade -1
INFO  [alembic.runtime.migration] Context impl PostgresqlImpl.
INFO  [alembic.runtime.migration] Will assume transactional DDL.
INFO  [alembic.runtime.migration] Running downgrade dd75a2adc1fa -> 6cf3090b1e09, add course schedule table
~\OneDrive\Desktop\CTS\git-local\cts_dn-5.0\3_db_integration\ho-7> 

Step 3 

Verify 

~\OneDrive\Desktop\CTS\git-local\cts_dn-5.0\3_db_integration\ho-7> psql -U postgres -h localhost -p 5432
Password for user postgres:

psql (16.11)
WARNING: Console code page (437) differs from Windows code page (1252)
         8-bit characters might not work correctly. See psql reference
         page "Notes for Windows users" for details.
Type "help" for help.

postgres=# \c college_db_orm
You are now connected to database "college_db_orm" as user "postgres".
college_db_orm=# \dt
              List of relations
 Schema |      Name       | Type  |  Owner
--------+-----------------+-------+----------
 public | alembic_version | table | postgres
 public | courses         | table | postgres
 public | departments     | table | postgres
 public | enrollments     | table | postgres
 public | professors      | table | postgres
 public | students        | table | postgres
(6 rows)


college_db_orm=# 

Step 4 

```bash
alembic current
```

~\OneDrive\Desktop\CTS\git-local\cts_dn-5.0\3_db_integration\ho-7> alembic current
INFO  [alembic.runtime.migration] Context impl PostgresqlImpl.
INFO  [alembic.runtime.migration] Will assume transactional DDL.
6cf3090b1e09
~\OneDrive\Desktop\CTS\git-local\cts_dn-5.0\3_db_integration\ho-7>     

** Risky Step **

Step 5

Back to base line before migrations 

```bash 
alembic downgrade base
```

~\OneDrive\Desktop\CTS\git-local\cts_dn-5.0\3_db_integration\ho-7> alembic downgrade base
INFO  [alembic.runtime.migration] Context impl PostgresqlImpl.
INFO  [alembic.runtime.migration] Will assume transactional DDL.
INFO  [alembic.runtime.migration] Running downgrade 6cf3090b1e09 -> afb3397da926, added is_active to students
INFO  [alembic.runtime.migration] Running downgrade afb3397da926 -> , initial schema

postgres=# \c college_db_orm;
You are now connected to database "college_db_orm" as user "postgres".
college_db_orm=# \dt
              List of relations
 Schema |      Name       | Type  |  Owner
--------+-----------------+-------+----------
 public | alembic_version | table | postgres
 public | courses         | table | postgres
 public | departments     | table | postgres
 public | enrollments     | table | postgres
 public | professors      | table | postgres
 public | students        | table | postgres
(6 rows)

college_db_orm=# \d students;
                                            Table "public.students"
     Column      |         Type          | Collation | Nullable |                   Default
-----------------+-----------------------+-----------+----------+----------------------------------------------
 student_id      | integer               |           | not null | nextval('students_student_id_seq'::regclass)
 first_name      | character varying(16) |           | not null |
 last_name       | character varying(16) |           | not null |
 email           | character varying(32) |           | not null |
 date_of_birth   | date                  |           |          |
 department_id   | integer               |           |          |
 enrollment_year | integer               |           |          |
Indexes:
    "students_pkey" PRIMARY KEY, btree (student_id)
    "students_email_key" UNIQUE CONSTRAINT, btree (email)
Foreign-key constraints:
    "students_department_id_fkey" FOREIGN KEY (department_id) REFERENCES departments(department_id)
Referenced by:
    TABLE "enrollments" CONSTRAINT "enrollments_student_id_fkey" FOREIGN KEY (student_id) REFERENCES students(student_id)

Step 6 

Back to head after all the migrations 

```bash 
alembic upgrade head
```

~\OneDrive\Desktop\CTS\git-local\cts_dn-5.0\3_db_integration\ho-7> alembic upgrade head
INFO  [alembic.runtime.migration] Context impl PostgresqlImpl.
INFO  [alembic.runtime.migration] Will assume transactional DDL.
INFO  [alembic.runtime.migration] Running upgrade  -> afb3397da926, initial schema
INFO  [alembic.runtime.migration] Running upgrade afb3397da926 -> 6cf3090b1e09, added is_active to students
INFO  [alembic.runtime.migration] Running upgrade 6cf3090b1e09 -> dd75a2adc1fa, add course schedule table
~\OneDrive\Desktop\CTS\git-local\cts_dn-5.0\3_db_integration\ho-7>    

Step 7 

Verify back to head??

~\OneDrive\Desktop\CTS\git-local\cts_dn-5.0\3_db_integration\ho-7> alembic current
INFO  [alembic.runtime.migration] Context impl PostgresqlImpl.
INFO  [alembic.runtime.migration] Will assume transactional DDL.
dd75a2adc1fa (head)
~\OneDrive\Desktop\CTS\git-local\cts_dn-5.0\3_db_integration\ho-7>                                      

