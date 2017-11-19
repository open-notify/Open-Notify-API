FLAKEIGNORE=E501,E241
PYTHONVERSION=python3.5

# Default: run a local dev server.
all: local

# The file `packages.txt` contains the names of the base packanges.
# Example: just `falcon`.
# To build a lockfile that defines an entire environment we install the named
# packages in `packages.txt` to a virtualenv, then run `$ pip freeze` to
# "lock" all the versions and sub-dependencies into a standard
# `requirements.txt` file.
# If you want to pin a package pin it in `packages.txt`!
requirements.txt: packages.txt
	virtualenv --python=`which $(PYTHONVERSION)` ./dummy_env
	./dummy_env/bin/pip install -r packages.txt
	./dummy_env/bin/pip freeze > requirements.txt
	rm -rf dummy_env

# Don't manually edit `requirements.txt`, but change `packages.txt` and
# generate `requirements.txt` from that.
# This builds a local "virtualenv" in the directory named `env`.
# Run python from here like this:
# $ ./env/bin/python
env: requirements.txt
	virtualenv --python=`which $(PYTHONVERSION)` ./env
	./env/bin/pip install -r requirements.txt
	touch env

# Run python setup.py install in the virtualenv
install: env
	./env/bin/python setup.py install

# Run a development server on port 5000
# Use this for testing, systemd dameonizes this in production.
local: install
	./env/bin/uwsgi --wsgi-file ./env/bin/server.py --callable api --http-socket 127.0.0.1:5000 --processes 1 --workers 1

# Get the latest TLE file over the network and store in Redis
update_tle: install
	./env/bin/update_tle.py

# update_iss runs a process forever (loop forever) updating the ISS position
# JSON to Redis once per second.
# Use this for testing, systemd dameonizes this in production
update_iss: install update_tle
	./env/bin/update_iss_position.py

# Push the "people in space" JSON to Redis for the server to use.
# Change the JSON in the file `update_astros.py` and run tp update.
update_astros: install
	./env/bin/update_astros.py

# Update the `patch` version (1.0.XX) of this project
patch: env
	./env/bin/bumpversion patch

# Build a debian package for deploying
build: env
	cd static; make
	./env/bin/gitchangelog > debian/changelog
	dpkg-buildpackage --unsigned-source --unsigned-changes --build=binary
	mv ../open-notify-api_*.deb ./

# pylint with flake
lint:
	flake8 --ignore $(FLAKEIGNORE) bin/server.py
	flake8 --ignore $(FLAKEIGNORE) bin/update_tle.py
	flake8 --ignore $(FLAKEIGNORE) bin/update_iss_position.py
	flake8 --ignore $(FLAKEIGNORE) bin/update_astros.py

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

.PHONY: clean lint build patch install update_astros update_iss update_tle local all
