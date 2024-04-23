dev:
	poetry run python manage.py runserver

install:
	poetry install

start:
	poetry run gunicorn --workers=4 hammer_test_case.wsgi

build:
	./build.sh