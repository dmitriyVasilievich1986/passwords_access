isort:
	python -m isort src
black:
	python -m black src
flake:
	python -m flake8 src
pylint:
	python -m pylint src
mypy:
	python -m mypy src
format: isort black flake pylint mypy
