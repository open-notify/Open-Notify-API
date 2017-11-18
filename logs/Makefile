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
	cat test.log | ./datadog-monitor.py

lint:
	flake8 --ignore $(FLAKEIGNORE) datadog-monitor.py
	flake8 --ignore $(FLAKEIGNORE) nginx_parse

clean:
	rm -rf dummy_env
	rm -rf env
