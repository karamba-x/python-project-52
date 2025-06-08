install:
	uv sync

build:
	./build.sh

collectstatic:
	python manage.py collectstatic --noinput

migrate:
	python manage.py migrate --noinput

test:
	uv run python manage.py test

dev:
	uv run python manage.py runserver

trans:
	uv run python manage.py makemessages -l ru

c-trans:
	uv run python manage.py compilemessages

render-start:
	gunicorn task_manager.wsgi