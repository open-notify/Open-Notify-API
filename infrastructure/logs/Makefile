FLAKEIGNORE=E501,E241
PYTHONVERSION=python3.5

all: test

requirements.txt: packages.txt
	virtualenv --python=`which $(PYTHONVERSION)` ./dummy_env
	./dummy_env/bin/pip install -r packages.txt
	./dummy_env/bin/pip freeze > requirements.txt
	rm -rf dummy_env

env: requirements.txt
	virtualenv --python=`which $(PYTHONVERSION)` ./env
	./env/bin/pip install -r requirements.txt
	touch env

test: env
	./env/bin/python setup.py install
	cat test.log | ./env/bin/datadog-monitor.py

build: env
	dpkg-buildpackage --unsigned-source --unsigned-changes --build=binary

lint:
	flake8 --ignore $(FLAKEIGNORE) datadog-monitor.py
	flake8 --ignore $(FLAKEIGNORE) nginx_parse

clean: build_clean
	rm -rf dummy_env
	rm -rf env

build_clean:
	rm -rf build
	rm -f  debian/debhelper-build-stamp
	rm -rf debian/open-notify-api-logs
	rm -f  debian/open-notify-api-logs.debhelper.*
	rm -f  debian/open-notify-api-logs.postinst.*
	rm -f  debian/open-notify-api-logs.substvars
	rm -f  debian/files
	rm -rf debian/.debhelper
	rm -f ../open-notify-api-logs*.*

.PHONY: clean build_clean lint build test
