# Open Nofity APIs

![](https://img.shields.io/badge/language-python%202-green.svg)
[![Build Status](https://travis-ci.org/open-notify/Open-Notify-API.svg)](https://travis-ci.org/open-notify/Open-Notify-API)
[![Requirements Status](https://requires.io/github/open-notify/Open-Notify-API/requirements.svg?branch=master)](https://requires.io/github/open-notify/Open-Notify-API/requirements/?branch=master)

APIs for [api.open-notify.org](http://api.open-notify.org)


## Install for the first time:

Make sure you have some packages:

    # apt-get install python python-dev python-pip virtualenvwrapper redis-server

Note: if you're installing `virtualenvwrapper` for the first time, be sure to log out and back in before continuing.

Create a virtual environment

    $ mkvirtualenv opennotify
    (opennotify)$ pip install -r requirements.txt

Get data

    (opennotify)$ python update.py


## Run locally:

Start virtual environment

    $ workon opennotify

Run with [foreman](https://github.com/ddollar/foreman) using dev procfile:

    (opennotify)$ foreman start -f Procfile.dev

Open a browser to [localhost:5000](http://localhost:5000).


## Run Testsuite

    (opennotify)$ cd testsuite
    (opennotify)$ pip install -r requirements.txt
    (opennotify)$ cd ..
    (opennotify)$ make test


## API Documentation

Docs are in the gh-pages branch, or on the web here:

 - [Open Notify API Documentation](http://open-notify.org/Open-Notify-API/)


## License

Copyright (C) 2016 Nathan Bergey

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program.  If not, see <http://www.gnu.org/licenses/>.
