# MySite
MySite is a simple web application built using Python and the Django framework. The site uses a Postgres database and implements all basic functionalities including create, read, update, and delete (CRUD) operations on the database records.

## Requirements
To run MySite, you will need:

Python 3.6 or higher
Django 3.2 or higher
psycopg2-binary (for working with Postgres)

## Installation
1. Clone the repository to your computer: git clone https://github.com/yourusername/mysite.git
2. Navigate to the mysite directory: cd mysite
3. Create and activate a virtual environment (optional but recommended): virtualenv env && source env/bin/activate
4. Install dependencies: pip install -r requirements.txt
5. Create a Postgres database and specify its details in mysite/settings.py file:

 DATABASES = {
   'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': 'bogdan2ko1',
        'USER': 'postgres',
        'PASSWORD': '',
       'HOST': 'localhost',
       'PORT': '5432',
    }
 }

6. Run migrations to create necessary tables in the database: python manage.py migrate
7. Start the local server: python manage.py runserver
8. After that, you can open a web browser and navigate to http://localhost:8000 to see MySite in action.
