.PHONY: all test flake8 docs up down reset-volume reset rebuild migrate makemigrations

MAKEFLAGS = silent

TEST_COMMAND = $(VIRTUAL_ENV)/bin/django-admin.py

DJANGO_SETTINGS_MODULE = pycon.settings.test

all: flake8 test

test:
	$(TEST_COMMAND) test --noinput --settings=$(DJANGO_SETTINGS_MODULE)

flake8:
	$(info ----Flake8 report----)
	@flake8 pycon
	@flake8 symposion

# If 'make docs' fails, try pip installing requirements/docs.txt
docs:
	(cd docs; DJANGO_SETTINGS_MODULE=$(DJANGO_SETTINGS_MODULE) make html)

up:
	@docker-compose up -d
	@docker-compose run web python manage.py migrate
	@docker-compose run web python manage.py loaddata fixtures/*.json
	@open http://localhost:8000

makemigrations:
	@docker-compose run web python manage.py makemigrations

migrate:
	@docker-compose run web python manage.py migrate

down:
	@docker-compose down
	@docker-compose rm

reset-volume:
	@docker volume rm pycon_pgdata

rebuild:
	@docker-compose build

reset: down rebuild reset-volume up

push-staging:
	@git fetch -a
	@git checkout staging
	@git merge origin/develop
	@git checkout develop
	@git push origin staging

push-production:
	@git fetch -a
	@git checkout production
	@git merge origin/develop
	@git checkout develop
	@git push origin production
