FLAKEIGNORE=E501,E241
PYTHONVERSION=python3

all: local

env: requirements.txt
	virtualenv --python=`which $(PYTHONVERSION)` ./env
	./env/bin/pip install -r requirements.txt
	touch env

run: env
	./env/bin/uwsgi --ini production.ini

local: env
	./env/bin/uwsgi --ini testing.ini

update_tle: env
	./env/bin/python update_tle.py

update_iss: env
	./env/bin/python update_iss_position.py

update_astros: env
	./env/bin/python update_astros.py

lint:
	flake8 --ignore $(FLAKEIGNORE) server.py
	flake8 --ignore $(FLAKEIGNORE) update_tle.py
	flake8 --ignore $(FLAKEIGNORE) update_iss_position.py
	flake8 --ignore $(FLAKEIGNORE) update_astros.py

clean:
	rm -rf env
