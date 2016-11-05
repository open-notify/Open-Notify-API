FLAKEIGNORE=E501,E241

all: local

lint:
	flake8 --ignore $(FLAKEIGNORE) server.py
	flake8 --ignore $(FLAKEIGNORE) update_tle.py
	flake8 --ignore $(FLAKEIGNORE) update_iss_position.py
	flake8 --ignore $(FLAKEIGNORE) update_astros.py

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
