PYTHON_INTERPRETER=python
PIP=pip
SHELL=/bin/bash
PYTHONPATH=$(shell pwd)

create-environment:
	$(PYTHON_INTERPRETER) -m venv venv

install-requirements: create-environment
	source venv/bin/activate && $(PIP) install -r requirements.txt

unit-test: install-requirements
	source venv/bin/activate && PYTHONPATH=$(PYTHONPATH) && pytest test/test_lambda_func.py -vvv

security-check: install-requirements
	source venv/bin/activate && bandit src/lambda_func.py && pip-audit -r ./requirements.txt

check-pep8-compliance: install-requirements
	source venv/bin/activate && flake8 src/lambda_func.py

run-checks: unit-test security-check check-pep8-compliance

uninstall-requirements: create-environment
	source venv/bin/activate && $(PIP) uninstall -r requirements.txt
