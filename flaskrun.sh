#!/bin/bash
cd /opt/
export FLASK_ENV=development
export FLASK_APP=main
flask run --host=0.0.0.0 --port=1111