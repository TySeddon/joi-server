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
    pip install munch

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

The following instructions depend on the Azure CLI.  https://docs.microsoft.com/en-us/cli/azure/install-azure-cli

1. az login
2. az extension add --name db-up
3. az postgres up --resource-group joi --location eastus --sku-name B_Gen5_1 --server-name joi-dbserver --database-name joi-db --admin-user <admin-username> --admin-password <admin-password> --ssl-enforcement Enabled
4. az webapp up --resource-group joi --location eastus --plan joi-plan --sku P1V2 --name joi-site
5. az webapp config appsettings set --settings DBHOST="joi-dbserver" DBUSER="<admin-username>" DBPASS="<admin-password>" DBNAME="joi-db"

Here is a line by line description:

1. Login to Azure with permissions to create and manage resources
2. Add an extension to Azure CLI to gain capability to create databases
3. Create a Postgres database in "joi-db" resource group in region "eastus".  Set the database admin username and password
4. Create a App Service website in the "joi-db" resource group in region "eastus"
5. Configure the App Settings from web site to contain database connection information

NOTE: Any of the above names (databases, resource groups, regions, etc) can be changed.  Just make the appropriate changes in the settings.py and production.py.

You now have a resource group, a database server, a database, and a website.  Code can be deployed from Visual Studio Code via the "az webapp up" command documented later in this document.

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
    az webapp up --runtime "PYTHON:3.9"

### Run Management Commands on Azure    
1. Open Azure Shell
    az webapp ssh
2. cd joiwebsite
3. Run commands such as:
    python manage.py migrate


## Chrome Configure
These instructions are for the Spotify Web Playback

### Allow Sound to Auto Play
Chrome does not allow videos to automatically play (autoplay).  This can be overridden in settings.
1. Open chrome
2. In URL type "chrome://settings/content/sound"
3. Under "Customized behaviors", "Allowed to play sound", click "Add" button
4. Enter the URLs that are allowed to auto play.
    * localhost:8000
    * URL for production (TBD)

### Play Protectect Content
1. In your browser address bar, enter chrome://settings/content
2. Under Protected content, switch on Allow site to play protected content.

### Install ???chrome widevine???
This upgrades browser on Raspberry Pi so that it can play Spotify
    sudo apt update
    sudo apt install libwidevinecdm0


# Reports

## Example of extracting JSON fields
    select 
        memorybox_session_media_id, 
        media_name, 
        media_artist,
        resident_motion, 
        json_extract_path(resident_motion::json,'percent') as motion_percent,
        json_extract_path(resident_motion::json,'num_of_seconds') as total_seconds_monitored,
        media_features,
        json_extract_path(media_features::json,'tempo') as tempo,
        json_extract_path(media_features::json,'danceability') as danceability,
        json_extract_path(media_features::json,'valence') as valence,
        json_extract_path(media_features::json,'energy') as energy
    from joi_memoryboxsessionmedia
    where resident_motion is not null
    order by media_end_datetime desc;

