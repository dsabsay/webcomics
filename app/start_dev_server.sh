#! /bin/bash

source venv/bin/activate
export FLASK_APP=webcomics
export FLASK_ENV=development
flask run
