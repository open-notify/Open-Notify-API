FLAKEIGNORE=E501,E241
PYTHONVERSION=python3.5

all: local

requirements.txt: packages.txt
	virtualenv --python=`which $(PYTHONVERSION)` ./dummy_env
	./dummy_env/bin/pip install -r packages.txt
	./dummy_env/bin/pip freeze > requirements.txt
	rm -rf dummy_env

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

patch: env
	./env/bin/bumpversion patch

build: env
	cd static; make
	./env/bin/gitchangelog > debian/changelog
	dpkg-buildpackage --unsigned-source --unsigned-changes --build=binary
	mv ../open-notify-api_*.deb ./

lint:
	flake8 --ignore $(FLAKEIGNORE) server.py
	flake8 --ignore $(FLAKEIGNORE) update_tle.py
	flake8 --ignore $(FLAKEIGNORE) update_iss_position.py
	flake8 --ignore $(FLAKEIGNORE) update_astros.py

clean:
	rm -rf dummy_env
	rm -rf env
	rm -f *.deb
	rm -rf debian/.debhelper
	rm -rf debian/open-notify-api
	rm -f debian/*.log
	rm -f debian/*.debhelper
	rm -f debian/*.substvars
	rm -f debian/debhelper-build-stamp
