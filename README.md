# To Install

Run `pip install -r requirements.txt`

# To run locally

Run `python manage.py runserver`

# To reset database

1. Delete `db.sqlite3` and all migration files (except `__init__.py`)
2. Run `python manage.py makemigrations`
3. Run `python manage.py migrate`.
4. Run `python manage.py seed`

# Database Notes:

Docket:
- Can have multiple fruit intakes
- Can have multiple crush orders

Fruit Intake:
- Each fruit intake has 1 docket (one to many relationship)

Crush Order:
- Can have multiple dockets (many to many relationship)
- Can be spread across multiple vessels (many to many relationship)

Vessels:
- Can gave multiple crush orders (many to many relationship)
