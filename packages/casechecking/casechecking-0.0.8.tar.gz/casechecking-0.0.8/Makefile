PYTHON := python3

test:
	$(PYTHON) -m pytest ./casechecking/

coverage:
	$(PYTHON) -m pytest --cov-report=term --cov=casechecking **/*_test.py

package:
	$(PYTHON) -m build

check:
	$(PYTHON) -m twine check dist/*

upload-test:
	$(PYTHON) -m twine upload --repository testpypi dist/*

upload:
	$(PYTHON) -m twine upload dist/*

dependencies:
	$(PYTHON) -m pip install pytest twine setuptools