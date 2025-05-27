build:
	./build.sh

render-start:
	gunicorn task_manager.wsgi

install:
	uv pip install --requirement pyproject.toml

collectstatic:
	python manage.py collectstatic --noinput

migrate:
	python manage.py migrate