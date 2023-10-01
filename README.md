A "social media" application built using the FastAPI web framework in Python and a PostgreSQL database.

# Setting up local development environment
Create a python virtual environment on windows:

```py -3 -m venv <name>``` 


while in virtual environment install required packages with pip:

```pip install -r requirements.txt```

To run web server locally using uvicorn (use --reload to automatically restart server when changes are made):

```uvicorn app.main:app --reload```

```{URL}/docs``` for API documentation

## environment variables and database

A running PostgreSQL database is needed. check congfig.py to see what environment variables are needed.

# Alembic
Alembic is a database migration tool to help make and track changes to DB schemas/tables as well as rollback changes when necessary. Alembic can automatically pull database changes from Sqlalchemy models and generate the proper instructions for the database driver.


After making any changes to Sqlalchemy models, a new revision or version can be created:

```alembic revision --autogenerate -m "<some-message>"```

To commit changes to the database run:

```alembic upgrade <version-name>``` or by upgrading to newest revision: ```alembic upgrade head```

