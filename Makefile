isort:
	python -m isort src
black:
	python -m black src
flake:
	python -m flake8 src
pylint:
	python -m pylint src
format: isort black flake pylint
