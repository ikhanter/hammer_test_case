dev:
	poetry run python manage.py runserver

install:
	poetry install

start:
	poetry run gunicorn hammer_test_case.wsgi

build:
	./build.sh