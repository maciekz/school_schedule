# school_schedule

School schedule task


# Author
[Maciej Zięba \<maciekz82@gmail.com\>](https://github.com/maciekz)


# Assumptions made

When working on the task, I have made the following assumptions:

 * Other API endpoints (for example, for management of the objects) were not mentioned in the task, so I did not create them.
 * The task does not provide any requirements or restrictions for the objects so I didn't add any but I believe that real-life application could provide for example:
    * Constraint for unique class names.
    * Constraint for a class to have only a single subject on a given day for a given hour.
    * Constraint for a teacher to have only a single subject with a given name.
 * Currently filtering by class_name uses exact match but depending on the requirements, it could be case insensitive.
 * day_of_week is stored in the database as an integer with the range of 0 (Monday) to 6 (Sunday) for faster sorting and filtering but when returning the data the endpoint provides human readable names.


# Possible improvements

The fact that school schedule usually does not change very often could allow for following performance improvements (if they are not against requirements):

1. Create a "search model" that would store all the required schedule information instead of gathering it "on the fly" (requiring joins, subqueries, etc.). Any changes to original models would update the "search models".

2. It should be possible to cache HTTP responses (for example using Varnish). This could drastically improve performance and the fact that a change would be reflected only after a few seconds, in most cases should not matter.


Also the Docker setup and configuration could be improved.


# Docker installation

Build the application with `docker-compose`:

```
sudo docker-compose build
```

Run required database migrations:

```
sudo docker-compose run web python src/manage.py migrate
```

## Running application

Start the application with `docker-compose`:

```
sudo docker-compose up
```

## Running application in development mode

Start the application with `docker-compose` using `docker-compose.dev.yml` configuration file:

```
sudo docker-compose -f docker-compose.dev.yml up
```

## Running tests

Run the tests with `docker-compose`:

```
sudo docker-compose run web pytest src/schedule/tests
```


# Local installation

Create a python virtualenv and activate it:

```
python -m venv venv
source ./venv/bin/activate
```

Install application and its dependencies:

```
pip install -e .
```

You can also install the application with various development tools:

```
pip install -e .[dev]
```

Run required database migrations:

```
python src/manage.py migrate
```

## Configuration

The application can be configured through `src/school_schedule/settings.py` file.

## Running application

To run the application, use the standard Django `runserver` command:

```
python src/manage.py runserver
```

## Running tests

To run the tests, use the `pytest` command:

```
pytest src/schedule/tests
```


# Usage

When using the default port `8000`, the endpoint is available at http://localhost:8000/schedule/

Example calls:

```
http://localhost:8000/schedule/
http://localhost:8000/schedule/for_today=true
http://localhost:8000/schedule/class_name=5A
http://localhost:8000/schedule/for_today=true&class_name=5A
```
