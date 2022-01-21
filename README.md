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

## Chrome Configure

### Allow Sound to Auto Play
Chromse does not allow videos to automatically play (autoplay).  This can be overridden in settings.
1. Open chrome
2. In URL type "chrome://settings/content/sound"
3. Under "Customized behaviors", "Allowed to play sound", click "Add" button
4. Enter the URLs that are allowed to auto play.
    * localhost:8000
    * URL for production (TBD)

