manage = poetry run python manage.py

compilemessages:
	$(manage) compilemessages

mkmg:
	$(manage) makemigrations
	$(manage) migrate

linter:
	isort server/
	flake8 server/

messages: compilemessages
	$(manage) makemessages --locale ru

run:
	$(manage) runserver

