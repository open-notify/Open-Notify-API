DEPS := $(shell find src -not -name ".*" -type f)

all: public

node_modules: package.json
	npm install

public: node_modules $(DEPS)
	./node_modules/.bin/gulp
	touch public

test_public: public
	./node_modules/.bin/superstatic public --port 8000 --debug true --gzip true

clean:
	rm -rf node_modules
	rm -rf public
