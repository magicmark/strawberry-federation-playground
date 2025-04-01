start:
	poetry run supervisord

black:
	poetry run black .

test: black