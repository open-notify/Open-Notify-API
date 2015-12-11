test:
	python ./run_tests.py
	honcho start

clean:
	find . -name "*.pyc" -type f -delete

lint:
	flake8 app.py
	flake8 iss.py
	flake8 update.py
	flake8 util.py
