# joi


## Virtual Environment Setup

### Install Virtual Environment
    pip install virtualenv

### Creating 
    python -m venv venv

### Activate Virtual Environment
    .\venv\Scripts\activate

# Required Packages
    python -m pip install Django


## Project Setup
These are tasks that were run when the project was setup.  These are being documented for learning purposes.

### Setup Website Project
    django-admin startproject joiwebsite  

### Setup Webstie App
    python manage.py startapp joi     


## Management Commands

### Run Development Web Server
    python manage.py runserver  

### Database Migration

#### Create Migration
Create a migration when you have changed model code
    python manage.py makemigrations joi

#### Apply Migrations
Apply outstanding migrations to the database
    python manage.py migrate     

#### Start Django Shell
    python manage.py shell

