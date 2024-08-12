.PHONY: install
install:
	poetry install

.PHONY: install_pre-commit
install_pre-commit:
	poetry run pre-commit uninstall
	poetry run pre-commit install

.PHONY: lint
lint:
	poetry run pre-commit run --all-files

.PHONY: light-lint
light-lint:
	poetry run pre-commit run

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

.PHONY: up-dependencies-only
up-dependencies-only:
	test -f .env || touch .env
	docker-compose -f docker-compose.dev.yml up --build

.PHONY: update
update: install migrations migrate install_pre-commit;
