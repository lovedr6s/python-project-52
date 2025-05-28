build:
	./build.sh

render-start:
	gunicorn task_manager.wsgi

install:
	uv pip install --requirement pyproject.toml

collectstatic:
	python manage.py collectstatic --noinput

migrate:
	docker compose run --rm app uv run python manage.py migrate