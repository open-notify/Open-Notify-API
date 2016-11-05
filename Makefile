all: local

lint:
	flake8 server.py
	flake8 update_tle.py
	flake8 update_iss_position.py

runenv: requirements.txt
	virtualenv --python=`which python3.4` ./runenv
	./runenv/bin/pip install -r requirements.txt
	touch runenv

run: runenv
	./runenv/bin/uwsgi --ini production.ini

local: runenv
	./runenv/bin/uwsgi --ini testing.ini
