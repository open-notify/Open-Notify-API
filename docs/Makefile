all: local

node_modules: package.json
	rm -rf node_modules
	npm install

local: node_modules
	./node_modules/.bin/superstatic

test: node_modules
	if npm test | grep "Project Errors"; \
    then npm test; exit 1;\
    fi

clean:
	rm -rf node_modules
