Create test db:
`docker-compose up -d test_db`

Create migration:
`PYTHONPATH=.. alembic revision --autogenerate -m "migration name"`

Run upgrade:
`PYTHONPATH=.. alembic upgrade head`

Run tests:
```
docker build -t family-service-base-img . && docker-compose -f ci/docker-compose.yml run tests 
```