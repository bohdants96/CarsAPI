# CarsAPI

Firstly, set your variables nearby example.env in file .env in same folder.

To run the project with docker, use:

`docker compose up`

or to run local, change variables to your local in .env, then run:

`pip install-r requirements.txt`

Run migrations for database:

`python manage.py migrate`

And start your server with command:

`python manage.py runserver`

For testing app, run:

`coverage run -m pytest`

And to check report, run:

`coverage report --show-missing`

Also you can generate some cars for database with:

`python manage.py generate_cars 10`

Or get some cars from internal service:

`python manage.py fetch_cars 10`