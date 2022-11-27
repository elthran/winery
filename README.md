# Development
See [Folder Structure](docs/Folder%20Structure.md)

## To Install

1. Run `pip install -r requirements.txt`

## To set up
1. Run `python manage.py makemigrations`
2. Run `python manage.py migrate`.
3. Run `python manage.py seed`

## To run locally

1. Run `python manage.py runserver`

## To reset database

1. Run `python manage.py reset`

This does:
1. Delete `db.sqlite3` and all migration files (except `__init__.py`)
2. Run `python manage.py makemigrations`
3. Run `python manage.py migrate`.
4. Run `python manage.py seed`

See [Database Notes](docs/Database%20Notes.md)


# Testing

- `python manage.py guard` - runs test watcher
- `python manage.py test` - runs tests once.

Docs at https://docs.djangoproject.com/en/4.1/topics/testing/overview/.

See [Test Folder Layout](docs/Test%20Folder%20Layout.md)

