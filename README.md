Create test db:
`docker-compose up -d test_db`

Create migration:
`PYTHONPATH=.. alembic revision --autogenerate -m "migration name"`

Run upgrade:
`PYTHONPATH=.. alembic upgrade head`
