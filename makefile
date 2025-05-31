build:
	./build.sh

render-start:
	gunicorn task_manager.wsgi

install:
	uv pip install -r requirements.txt

collectstatic:
	uv run python manage.py collectstatic --noinput

migrate:
	uv run python manage.py migrate