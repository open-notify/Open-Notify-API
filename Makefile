all: local

lint:
	flake8 server.py
	flake8 update_tle.py
	flake8 update_iss_position.py
	flake8 update_astros.py

runenv: requirements.txt
	virtualenv --python=`which python3.4` ./runenv
	./runenv/bin/pip install -r requirements.txt
	touch runenv

run: runenv
	./runenv/bin/uwsgi --ini production.ini

local: runenv
	./runenv/bin/uwsgi --ini testing.ini

update_tle: runenv
	./runenv/bin/python update_tle.py

update_iss: runenv
	./runenv/bin/python update_iss_position.py

update_astros: runenv
	./runenv/bin/python update_astros.py
