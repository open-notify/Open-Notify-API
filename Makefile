all: local

runenv: requirements.txt
	virtualenv --python=`which python3.4` ./runenv
	./runenv/bin/pip install -r requirements.txt
	touch runenv

run: runenv
	./runenv/bin/uwsgi --ini production.ini

local: runenv
	./runenv/bin/uwsgi --ini testing.ini
