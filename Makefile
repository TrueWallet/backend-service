up:
	@docker-compose up -d
	@docker images -q -f dangling=true | xargs docker rmi -f

up-light:
	@docker-compose up -d postgres
	@docker images -q -f dangling=true | xargs docker rmi -f

down:
	@docker-compose down

ps:
	@docker-compose ps

run:
	@DJANGO_READ_DOT_ENV_FILE=1 python manage.py runserver 0.0.0.0:8000

ifeq (test-without-docker,$(firstword $(MAKECMDGOALS)))
  RUN_ARGS := $(wordlist 2,$(words $(MAKECMDGOALS)),$(MAKECMDGOALS))
  $(eval $(RUN_ARGS):;@:)
endif
test:
	@DJANGO_READ_DOT_ENV_FILE=1 python manage.py test $(RUN_ARGS) --settings=config.settings.test

validate:
	@DJANGO_READ_DOT_ENV_FILE=1 pre-commit run --all-files -c .pre-commit-config.yaml

ifeq (makemigrations,$(firstword $(MAKECMDGOALS)))
  RUN_ARGS := $(wordlist 2,$(words $(MAKECMDGOALS)),$(MAKECMDGOALS))
  $(eval $(RUN_ARGS):;@:)
endif
makemigrations:
	@DJANGO_READ_DOT_ENV_FILE=1 python manage.py makemigrations $(RUN_ARGS)

ifeq (migrate,$(firstword $(MAKECMDGOALS)))
  RUN_ARGS := $(wordlist 2,$(words $(MAKECMDGOALS)),$(MAKECMDGOALS))
  $(eval $(RUN_ARGS):;@:)
endif
migrate:
	@DJANGO_READ_DOT_ENV_FILE=1 python manage.py migrate $(RUN_ARGS)
