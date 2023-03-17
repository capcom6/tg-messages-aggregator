init:
	pip install -r requirements.txt

init-dev: init
	pip install -r requirements-dev.txt

start:
	python -m app

start-api:
	python -m app start

.PHONY: init init-dev start