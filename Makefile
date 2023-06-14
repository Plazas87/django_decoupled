-include .env
export

DJANGO_PRODUCTION_SETTINGS_MODULE = ${DJANGO_SETTINGS_MODULE}
IFACE ?= 127.0.0.1
PORT  ?= 8000

ifeq ($(OS),Windows_NT)
	OPEN_CMD = cmd /c start
else
	UNAME_S := $(shell uname -s)
	ifeq ($(UNAME_S),Linux)
		OPEN_CMD = xdg-open
	endif
	ifeq ($(UNAME_S),Darwin)
		OPEN_CMD = open
	endif
endif

#----------General----------#

# Extract arguments of the subcommand
.PHONY: _run_args
_run_args:
  # use the rest as arguments for the subcommand
  RUN_ARGS := $(wordlist 2,$(words $(MAKECMDGOALS)),$(MAKECMDGOALS))
  # ...and turn them into do-nothing targets
  $(eval $(RUN_ARGS):;@:)

# target: help - Display callable targets.
.PHONY: help
help:
	@egrep "^# target:" [Mm]akefile


########-------Django decoupled app-------########

#----------Docker Database----------#

# target: initdb - Initialize the database container
.PHONY: initdb
initdb:
	docker run -d --name django_decoupled_db \
		-v django_decoupled_data:/var/lib/postgresql/data \
		-p 5432:5432 \
		-e POSTGRES_HOST_AUTH_METHOD=trust \
		postgres:14

# target: createdb - Create the Database
.PHONY: createdb
createdb:
	docker exec -it django_decoupled_db createdb -U postgres django_decoupled

# target: startdb - Start a postgres database for the django_decoupled
.PHONY: startdb
startdb:
	docker start django_decoupled_db

# target: stopdb - Stop the django_decoupled postgres database
.PHONY: stopdb
stopdb:
	docker stop django_decoupled_db


# target: start - Start the apliaction using Docker containers
.PHONY: start
start:
	docker-compose up --build



#----------Django commands----------#

# target: clean_pyc - Remove all ".pyc" files
.PHONY: clean_pyc
clean_pyc:
	poetry run python -m django_decoupled.controllers.manage clean_pyc --path=src/django_decoupled

# target: createsuperuser - Create a super user account
.PHONY: createsuperuser
createsuperuser:
	poetry run python -m django_decoupled.controllers.manage createsuperuser

# target: shell_plus - Enter interactive environment
.PHONY: shell_plus
shell_plus:
	poetry run python -m django_decoupled.controllers.manage shell_plus

# target: makemigrations - Create migration files
# and migrate database models
.PHONY: makemigrations
makemigrations:
	poetry run python -m django_decoupled.controllers.manage makemigrations

# target: lstart - Start the application
.PHONY: lstart
lstart:
	poetry run python -m django_decoupled.controllers.manage runserver $(IFACE):$(PORT)

# target: run - Executes any of the available django commands
.PHONY: run
run: _run_args
	poetry run python -m django_decoupled.controllers.manage $(RUN_ARGS)
