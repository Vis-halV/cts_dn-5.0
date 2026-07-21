import os
import time

import psycopg2


conn = psycopg2.connect(
    host=os.getenv("DB_HOST", "localhost"),
    port=os.getenv("DB_PORT", "5432"),
    user=os.getenv("DB_USER", "postgres"),
    password=os.getenv("DB_PASSWORD", "9833"),
    dbname=os.getenv("DB_NAME", "college_db"),
)

cursor = conn.cursor()

start = time.time()
query_count = 1

cursor.execute("SELECT enrollment_id, student_id, course_id FROM enrollments")
enrollments = cursor.fetchall()

for enrollment in enrollments:
    cursor.execute(
        "SELECT first_name, last_name FROM students WHERE student_id = %s",
        (enrollment[1],),
    )
    cursor.fetchone()
    query_count += 1

end = time.time()

print("N+1: Queries Executed -", query_count)
print("Time:", end - start)

start = time.time()

cursor.execute(
    """
    SELECT
        s.first_name,
        s.last_name,
        c.course_name
    FROM enrollments e
    JOIN students s ON e.student_id = s.student_id
    JOIN courses c ON e.course_id = c.course_id
    """
)

rows = cursor.fetchall()

end = time.time()

print("Join: Queries Executed - 1")
print("Rows Returned -", len(rows))
print("Time:", end - start)

cursor.close()
conn.close()

"""

~\OneDrive\Desktop\CTS\git-local\cts_dn-5.0> py Module3_DatabaseIntegration\ho-4\n_plus_one.py
N+1: Queries Executed - 9
Time: 0.0027642250061035156
Join: Queries Executed - 1
Rows Returned - 8
Time: 0.0010771751403808594
~\OneDrive\Desktop\CTS\git-local\cts_dn-5.0>      

"""