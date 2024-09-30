install:
	# intall dependencies
	pip install --upgrade pip && pip install -r requirements.txt

format:
	# format code
	black *.py */*.py

lint:
	# flake8 or Pylint
	pylint --disable=R,C *.py

makemigrations:
	# make migrations
	python manage.py makemigrations

cleanmigrations:
	# clean migrations
	find -wholename "*/migrations/*.py" -not -name "__init__.py" -delete

migrate:
	# migrate
	python manage.py migrate

collectstatic:
	# collect static files
	python manage.py collectstatic --noinput

test-run:
	# run tests
	python manage.py test

test-coverage:
	# test coverage
	coverage run manage.py test -v 2 && coverage html

all: install format lint makemigrations migrate collectstatic test-coverage

rundev:
	python3 manage.py runserver

runprod:
	gunicorn --bind 0.0.0.0:8000 -w 4 --timeout 120 config.wsgi