# Project

Django Assessment


## Project Setup

### Environment Settings

create a .env file on the root and paste below variables init.
```
PROJECT_NAME=Assessment
PROJECT_SLUG=Django-Assessment
SERVER_URL=http://127.0.0.1:8000
```

### Requirements

```shell
pip install -r requirements/local.txt
```

## Basic Commands

### Follow below commands to start project on local machine 

- Create virtual env:

        python3 -m pip install virtualenv

- Activate virtual env:

        python3 -m virtualenv .venv

- Activate environment:
        
        . .venv/bin/activate

- Install requirements:
        
        pip install -r requirements/local.txt

- Start Server:
        
        python manage.py runserver


### To run test cases, hit below command in to the environment activated terminal 

- Create virtual env:

        python manage.py test