# Open Nofity APIs

APIs for [api.open-notify.org](http://api.open-notify.org)

## Install for the first time:

Make sure you have some packages:

    # apt-get install python python-dev python-pip virtualenvwrapper redis-server

Create a virtual environment

    $ mkvirtualenv opennotify
    (opennotify)$ pip install -r requirements.txt

Get data

    (opennotify)$ python update.py


## Run locally:

Start virtual environment

    $ workon opennotify

Start flask server

    (opennotify)$ python app.py

Go to [localhost:5000](http://localhost:5000)
