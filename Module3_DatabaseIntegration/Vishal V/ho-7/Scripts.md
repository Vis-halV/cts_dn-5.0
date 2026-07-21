# Scripts 

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
