.PHONY: install
install:
	poetry install

.PHONY: migrations
migrations:
	poetry run python -m blackshakara.manage makemigrations

.PHONY: migrate
migrate:
	poetry run python -m blackshakara.manage migrate

.PHONY: run-server
run-server:
	poetry run python -m blackshakara.manage runserver

.PHONY: superuser
superuser:
	poetry run python -m blackshakara.manage createsuperuser

.PHONY: update
update: install migrate ;
