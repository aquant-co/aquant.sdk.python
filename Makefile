start-dev:
	uvicorn app.main:app --reload

start:
	uvicorn app.main:app

migration-revision:
	alembic revision --autogenerate -m 

migration-gen:
	alembic upgrade head