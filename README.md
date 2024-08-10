# Inforce Python Task
## Task Description
A company needs internal service for its 'employees which helps them to
make a decision at the lunch place. Each restaurant will be uploading menus
using the system every day over API.

Employees will vote for the menu before leaving for lunch on a mobile app
for whom the backend has to be implemented. There are users who did not
update the app to the latest version and the backend has to support both
versions. The mobile app always sends the build version in headers

### API Functionality
- Authentication
- Creating restaurant
- Uploading menu for restaurant (There should be a menu for each day)
- Creating employee
- Getting current day menu
- Getting results for the current day

### Requirements
- Only Back End (no needs to add UI);
- REST architecture;
- Tech stack: Django + DRF, JWT, PostgreSQL, Docker(docker-compose), PyTests;
- Added at least a few different tests;
- README.md with a description of how to run the system;
- Will be a + to add flake8 or smth similar

## Project Setup
### Configuration
1. In root directory create file `.env.dev`. 

2. Create next key-value pairs:
    - SECRET_KEY=`your django secret key` (Could be any random string. You can use `get_random_secret_key` function from `django.core.management.utils`)
    - DEBUG=`1`
    - SQL_ENGINE=`django.db.backends.postgresql`
    - SQL_DATABASE=`your_db_name`
    - SQL_USER=`your_db_user`
    - SQL_PASSWORD=`your_db_password`
    - SQL_HOST=`db`
    - SQL_PORT=`5432`

### Docker
1. Windows:
    - Install [Docker Desktop](https://www.docker.com/products/docker-desktop/) 
    - Open downloaded program
    - Verify docker installation with command: `docker-compose -v`
    - In project's root run command: `docker-compose build` to build a docker image
    - After build successfully completed run command: `docker-compose up`

2. Linux:
    - Install [Docker](https://docs.docker.com/engine/install/ubuntu/#installation-methods)
    - Install docker compose plugin: `sudo apt-get install docker-compose-plugin`
    - In project's root run command: `docker compose build` to build a docker image
    - After build successfully completed run command: `docker compose up`

## Tests
In root directory run command: `pytest daily_menu`

### Tests Coverage
There is still a lot of functionality which should be tested, but I don't have anymore time to write them unfortunetly.

## Issues
1. I didn't quite understand the part about **"the backend has to support both versions of the app"**.
Since I don't know the actuall difference between "previous" app version and "current" to change my endpoints logic accordingly, 
therefore I didn't implement that.
2. I think I did probably way more than actuall task required, since I created all CRUD operations for each model. I guess,
that's why it took me so long. That was bad idea, but without this functionality the project wasn't looking good for me, so that's
my fault anyway.
