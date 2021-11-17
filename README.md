# Primaria World
### Primaria World is a virtual pet site that began in September 2017. You can adopt and raise a pet of your own, without any of the cleanup or expensive care products. There are many species, colors, and patterns to discover, and many more features to play with, so join today to try it all out!


## Features
- Choose from 10 adorable creatures in many different colors
- Take care of your pets' hunger, wellness, and happiness
- Collect all the items: plushies, books, trading cards, and more
- Complete quests for the Gods & Goddesses of the world
- Play games and earn points
- Be social on the boards, messages, and trades

## Roadmap
- [ ] Instant messaging
- [ ] New and improved world map
- [ ] Online trading card game

## Local Installation
- Make sure you have Python2 & pip installed

### Create Python2 Virtualenv
- `python2 -m virtualenv venv`
- Add variables to beginning of `venv/bin/activate`:
    - `export SECRET_KEY='your_secret_key_here`
    - `export DB_NAME='your_database_name_here`
    - `export DB_USER='your_database_username_here`
    - `export DB_PASS='your_database_password_here`
    - `export DB_HOST='your_database_hostname_here` (e.g. localhost)

#### Start Virtualenv
- `source venv/bin/activate`

### Install Dependencies
- `brew install rabbitmq` (macOS)
- `pip install django==1.9.6`
- `pip install setuptools==44.1.1`
- `pip install anyjson==0.3.3`
- `pip install celery==3.1.25`
- `pip install psycopg2-binary` (macOS)
- `pip install django-celery==3.2.1`
- `pip install django-compressor==2.0`
- `pip install django-sass-processor==0.5.3`

### Create Database
- Create `primaria` database in Postgres
- Alter `venv/bin/activate` with your own database details

### Migrate Database
- `python manage.py migrate`

### Load DB Data
- `python manage.py makemigrations`
- `python manage.py migrate`
- `python manage.py loaddata db.json`

### Start Celery Workers
- `brew services start rabbitmq`
- `python manage.py celery worker`
- `python manage.py celery beat`

### Start Server
- `python manage.py createsuperuser` (optional)
- `python manage.py runserver`

