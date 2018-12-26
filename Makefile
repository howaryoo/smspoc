SHELL := $(shell which bash)
PROJECT := sms

init:
	git config core.ignorecase false
	git config core.hooksPath .githooks

clean:
	find . -name '*.py[co]' -delete
	find . -name '.coverage*' -delete
	rm -rf build dist $(PROJECT).egg-info
	find . -path '*/__pycache__*' -delete
	find . -path '*/.pytest_cache*' -delete
	rm -rf report

validate: clean
	flake8 $(PROJECT)

test-unit: clean
	export PYTHONPATH=.:$(PYTHONPATH) && \
	py.test --durations=10 -s -v -m "not integration" test \
		--cov $(PROJECT) \
		--cov-report xml:cov.xml

test: clean
	export PYTHONPATH=.:$(PYTHONPATH) && \
	py.test --durations=10 -s -v test \
		--cov $(PROJECT) \
		--cov-report xml:cov.xml

build-prod: clean
	docker build  . -t $(PROJECT):latest


build: build-prod
	docker-compose build


up: build
	docker-compose up -d


%:
	@:
