# Joi Server
This is part of the Joi project for University of Southern Indiana.
The code in this repository holds server-side components such as the website and database.

## Technologies
* Python
* Django
* Postgres SQL
* Azure

## Development Workstation Setup
* Install Visual Studio Code
* Install Python 3.9+
* Install Azure CLI - https://docs.microsoft.com/en-us/cli/azure/install-azure-cli-windows?tabs=azure-cli
* Install Postgres SQL
* Setup Virtual Environment (see below)

## Virtual Environment Setup

### Install Virtual Environment
    pip install virtualenv

### Creating 
    python -m venv venv

### Activate Virtual Environment
    .\venv\Scripts\activate

# Required Packages
    pip install 'django==3.2.11'
    pip install psycopg2
    pip install whitenoise
    pip install djangorestframework
    pip install pyyaml
    pip install django-filter

## Update requirements.txt
    pip freeze > requirements.txt


## Project Setup
These are tasks that were run when the project was setup.  These are being documented for learning purposes.

### Create Website Project
    django-admin startproject joiwebsite  

### Create Webstie App
    python manage.py startapp joi     

## Azure One-Time Setup
Setup Django and Postgres on Azure - https://docs.microsoft.com/en-us/azure/app-service/tutorial-python-postgresql-app?tabs=bash%2Cclone&pivots=postgres-single-server

* az login
* az extension add --name db-up
* az postgres up --resource-group joi --location eastus --sku-name B_Gen5_1 --server-name cognivista-joi --database-name joi-test --admin-user <admin-username> --admin-password <admin-password> --ssl-enforcement Enabled
* az webapp up --resource-group joi --location eastus --plan joi-test-plan --sku B1 --name joi-test-site
* az webapp config appsettings set --settings DBHOST="cognivista-joi" DBUSER="<admin-username>" DBPASS="EryFe3hB2C_Q" DBNAME="<admin-password>"
* az webapp ssh


### Custom Startup Command
Because the Django project is not organized the way Azure wants, set the Startup Command of the web app.  This is located in Configuration, General settings on the Azure Portal.
    gunicorn --bind=0.0.0.0 --timeout 600 --chdir joiwebsite joiwebsite.wsgi

## Management Commands

### Run Development Web Server
    python manage.py runserver  

### Start Django Shell
    python manage.py shell

### Run Tests
    python manage.py test

### Create Database Migration
Create a migration when you have changed model code
    python manage.py makemigrations joi

### Apply Database Migrations
Apply outstanding migrations to the database
    python manage.py migrate   

### Custom Management Commands
python manage.py delete_data
python manage.py initialize_data      

### Redeploy code to Azure
    az webapp up


## Chrome Configure
These instructions are for the Spotify Web Playback

### Allow Sound to Auto Play
Chromse does not allow videos to automatically play (autoplay).  This can be overridden in settings.
1. Open chrome
2. In URL type "chrome://settings/content/sound"
3. Under "Customized behaviors", "Allowed to play sound", click "Add" button
4. Enter the URLs that are allowed to auto play.
    * localhost:8000
    * URL for production (TBD)

### Play Protectect Content
1. In your browser address bar, enter chrome://settings/content
2. Under Protected content, switch on Allow site to play protected content.

### Install “chrome widevine”
This upgrades browser on Raspberry Pi so that it can play Spotify
    sudo apt update
    sudo apt install libwidevinecdm0