build:
	./build.sh

render-start:
	gunicorn task_manager/task_manager.wsgi

install:
	uv pip install --requirement pyproject.toml

collectstatic:
	python task_manager/manage.py collectstatic --noinput

migrate:
	python task_manager/manage.py migrate