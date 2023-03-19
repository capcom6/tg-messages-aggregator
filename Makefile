init:
	pip install -r requirements.txt

init-dev: init
	pip install -r requirements-dev.txt

start:
	python -m app

start-api:
	python -m app start

start-bot:
	python -m app bot

.PHONY: init init-dev start start-api start-bot