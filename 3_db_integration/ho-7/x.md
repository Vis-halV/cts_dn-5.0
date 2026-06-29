### Step 106 · Roll back to base (remove ALL migrations)

> ⚠️ This drops every table Alembic manages. In a real project, always back up first.

```bash
alembic downgrade base
```

**Expected output:**
```
INFO  [alembic.runtime.migration] Running downgrade b2c3d4e5f6a7 -> a1b2c3d4e5f6, add is_active to students
INFO  [alembic.runtime.migration] Running downgrade a1b2c3d4e5f6 -> , initial schema
```

**Verify:**

```sql
\dt
-- Only alembic_version remains — all 5 model tables are gone
```

```bash
alembic current
# Output: (no current revision)  ← nothing applied
```

---

### Step 107 · Re-apply all migrations back to head

```bash
alembic upgrade head
```

**Expected output (all 3 revisions re-applied in order):**
```
INFO  [alembic.runtime.migration] Running upgrade  -> a1b2c3d4e5f6, initial schema
INFO  [alembic.runtime.migration] Running upgrade a1b2c3d4e5f6 -> b2c3d4e5f6a7, add is_active to students
INFO  [alembic.runtime.migration] Running upgrade b2c3d4e5f6a7 -> zzzzzzzzzzzz, add course schedule table
```

**Final verification:**

```bash
alembic current
# Output: zzzzzzzzzzzz (head)  ← back to latest ✓
```

```sql
\dt
-- departments, students, courses, enrollments,
-- professors, course_schedules all present ✓

\d students
-- is_active column present ✓

SELECT * FROM alembic_version;
-- shows zzzzzzzzzzzz ✓
```

---

### Step 108 (Bonus) · Django Migrations Equivalent

If using Django, the exact same workflow maps like this:

| Alembic | Django |
|---|---|
| `alembic init migrations` | Built-in, no setup needed |
| Edit `models.py` | Edit `models.py` in your app |
| `alembic revision --autogenerate -m "msg"` | `python manage.py makemigrations` |
| `alembic upgrade head` | `python manage.py migrate` |
| `alembic history` | `python manage.py showmigrations` |
| `alembic downgrade -1` | `python manage.py migrate <app> <previous_migration_name>` |
| `alembic downgrade base` | `python manage.py migrate <app> zero` |

**Django rollback example:**

```bash
# See migration history
python manage.py showmigrations myapp

# Roll back to just before the is_active migration
python manage.py migrate myapp 0001_initial

# Re-apply everything
python manage.py migrate
```

---

## Rollback Strategy Summary

| Command | What it does |
|---|---|
| `alembic upgrade head` | Apply all pending migrations |
| `alembic upgrade +1` | Apply exactly one next migration |
| `alembic downgrade -1` | Undo the most recent migration |
| `alembic downgrade base` | Undo ALL migrations (empty schema) |
| `alembic downgrade <hash>` | Roll back to a specific revision |
| `alembic current` | Show currently applied revision |
| `alembic history --verbose` | Show full revision chain |

---

## Common Errors & Fixes

| Error | Cause | Fix |
|---|---|---|
| `Can't locate revision identified by ...` | Migration file deleted but DB still has hash | Delete row from `alembic_version` and re-run |
| `Target database is not up to date` | Unapplied migrations exist | Run `alembic upgrade head` first |
| `Autogenerate produces empty migration` | DB already matches models | Expected — commit the empty file as a checkpoint |
| `ModuleNotFoundError: models` | `sys.path` not set in `env.py` | Add the `sys.path.insert` block shown in Step 94 |
| `Column already exists` | Running upgrade on existing schema | Drop tables manually or use `--autogenerate` to detect the drift |

---

## Complete Command Reference

```bash
# One-time setup
pip install alembic
alembic init migrations

# Generate a migration
alembic revision --autogenerate -m "describe the change"

# Apply migrations
alembic upgrade head       # all pending
alembic upgrade +1         # one step forward

# Roll back
alembic downgrade -1       # one step back
alembic downgrade base     # all the way back

# Inspect
alembic current            # current revision
alembic history --verbose  # full chain
alembic heads              # latest revision(s)
```