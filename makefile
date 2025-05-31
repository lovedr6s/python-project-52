build:
	./build.sh

render-start:
	uv run gunicorn task_manager.wsgi

install:
	uv pip install --requirement pyproject.toml

collectstatic:
	uv run python manage.py collectstatic --noinput

migrate:
	uv run python manage.py migrate