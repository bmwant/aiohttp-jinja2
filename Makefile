# Some simple testing tasks (sorry, UNIX only).

flake:
	flake8 japronto_jinja2 tests

test: flake
	py.test -s ./tests/

coverage:
	pytest --cov=japronto_jinja2 --cov-report=html --cov-report=term ./tests/
	@echo "open file://`pwd`/htmlcov/index.html"

clean:
	rm -rf `find . -name __pycache__`
	rm -f `find . -type f -name '*.py[co]' `
	rm -f `find . -type f -name '*~' `
	rm -f `find . -type f -name '.*~' `
	rm -f `find . -type f -name '@*' `
	rm -f `find . -type f -name '#*#' `
	rm -f `find . -type f -name '*.orig' `
	rm -f `find . -type f -name '*.rej' `
	rm -f .coverage
	rm -rf coverage
	rm -rf build
	rm -rf cover

release: clean
	python setup.py sdist
	python setup.py bdist_wheel
	twine upload -r pypi dist/*

doc:
	make -C docs html
	@echo "open file://`pwd`/docs/_build/html/index.html"

.PHONY: all build venv flake test release coverage clean doc
