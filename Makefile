
install:
	pip install -e .[test]

test:
	py.test

retest:
	py.test -vvv --lf

coverage:
	py.test --cov=labd.localemiddleware --cov-report=term-missing --cov-report=html

release:
	rm -rf dist/*
	python setup.py sdist bdist_wheel
	twine upload dist/*
