Step 1 

pip install alembic

Step 2

alembic init migrations

~\git-local\cts_dn-5.0\3_db_integration\ho-7> tree /f
Folder PATH listing for volume Windows-SSD
Volume serial number is 000000F2 A8A7:89E4
C:.
│   crud.py
│   models.py
│   requirements.txt

~\git-local\cts_dn-5.0\3_db_integration\ho-7>alembic init migrations

~\git-local\cts_dn-5.0\3_db_integration\ho-7> tree /f
Folder PATH listing for volume Windows-SSD
Volume serial number is 000000F2 A8A7:89E4
C:.
│   alembic.ini
│   crud.py
│   models.py
│   README.md
│   requirements.txt
│   x.md
│
└───migrations
    │   env.py
    │   README
    │   script.py.mako
    │
    └───versions
~\git-local\cts_dn-5.0\3_db_integration\ho-7>  

Step 3

Open `alembic.ini` and replace this line:

```ini
sqlalchemy.url = driver://user:pass@localhost/dbname
```

```ini
sqlalchemy.url = postgresql+psycopg2://postgres:your_password@localhost:5432/college_db_orm
```

your_password as your password 

Step 4 

Open `migrations/env.py`. Find these two lines near the top:

```python
target_metadata = None    # ← find this line
```

```python
target_metadata = Base.metadata  
```

Step 5

Add import 

```python
import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from models import Base
```

Step 6 


Generate the first (baseline) migration

```bash
alembic revision --autogenerate -m "initial schema"
```

~\git-local\cts_dn-5.0\3_db_integration\ho-7> alembic revision --autogenerate -m "initial schema"
INFO  [alembic.runtime.migration] Context impl PostgresqlImpl.
INFO  [alembic.runtime.migration] Will assume transactional DDL.
INFO  [alembic.runtime.plugins] setting up autogenerate plugin alembic.autogenerate.schemas
INFO  [alembic.runtime.plugins] setting up autogenerate plugin alembic.autogenerate.tables
INFO  [alembic.runtime.plugins] setting up autogenerate plugin alembic.autogenerate.types
INFO  [alembic.runtime.plugins] setting up autogenerate plugin alembic.autogenerate.constraints
INFO  [alembic.runtime.plugins] setting up autogenerate plugin alembic.autogenerate.defaults
INFO  [alembic.runtime.plugins] setting up autogenerate plugin alembic.autogenerate.comments
INFO  [alembic.ddl.postgresql] Detected sequence named 'students_student_id_seq' as owned by integer column 'students(student_id)', assuming SERIAL and omitting
INFO  [alembic.ddl.postgresql] Detected sequence named 'courses_course_id_seq' as owned by integer column 'courses(course_id)', assuming SERIAL and omitting
INFO  [alembic.ddl.postgresql] Detected sequence named 'enrollments_enrollment_id_seq' as owned by integer column 'enrollments(enrollment_id)', assuming SERIAL and omitting
INFO  [alembic.ddl.postgresql] Detected sequence named 'departments_department_id_seq' as owned by integer column 'departments(department_id)', assuming SERIAL and omitting
INFO  [alembic.ddl.postgresql] Detected sequence named 'professors_professor_id_seq' as owned by integer column 'professors(professor_id)', assuming SERIAL and omitting
Generating ~\git-local\cts_dn-5.0\3_db_integration\ho-7\migrations\versions\afb3397da926_initial_schema.py ...  done
~\git-local\cts_dn-5.0\3_db_integration\ho-7>       

Step 7

Apply the migration to the database

```bash 
alembic upgrade head
```

~\git-local\cts_dn-5.0\3_db_integration\ho-7> alembic upgrade head
INFO  [alembic.runtime.migration] Context impl PostgresqlImpl.
INFO  [alembic.runtime.migration] Will assume transactional DDL.
INFO  [alembic.runtime.migration] Running upgrade  -> afb3397da926, initial schema
~\git-local\cts_dn-5.0\3_db_integration\ho-7>      

Step 8 

Verify 

~\git-local\cts_dn-5.0\3_db_integration\ho-7> psql -U postgres -h localhost -p 5432
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


college_db_orm=# SELECT * FROM alembic_version;
 version_num
--------------
 afb3397da926
(1 row)


college_db_orm=# /q
college_db_orm-# \q
~\git-local\cts_dn-5.0\3_db_integration\ho-7> alembic current
INFO  [alembic.runtime.migration] Context impl PostgresqlImpl.
INFO  [alembic.runtime.migration] Will assume transactional DDL.
afb3397da926 (head)
~\git-local\cts_dn-5.0\3_db_integration\ho-7>  
