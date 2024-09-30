# Django Task Assignment

## Project Setup

### Install the dependencies:

    make install
or

    pip install -r requirements.txt

### Create migration Files:

    make makemigrations
or

    python manage.py makemigrations

### Apply migrations:

    make migrate
or

    python manage.py migrate

### Run the server:

    make rundev
or 

    python manage.py runserver

## Test Coverage

Run tests:
If you want to just run the tests simply run:

    make test-run
or

    python manage.py test
    
for getting the test coverage results run:
    
    make test-coverage
or

    coverage run manage.py test -v 2 && coverage html
you can see the results in  htmlcov/index.html

![test_coverage](https://github.com/user-attachments/assets/3862d727-5362-488b-856a-7574d975a7d8)
