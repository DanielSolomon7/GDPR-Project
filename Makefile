PYTHON_INTERPRETER=python
PIP=pip
SHELL=/bin/bash
PYTHONPATH=$(shell pwd)

create-environment:
	$(PYTHON_INTERPRETER) -m venv venv

install-requirements: create-environment
	source venv/bin/activate && $(PIP) install -r requirements.txt

unit-test: install-requirements
	source venv/bin/activate && PYTHONPATH=$(PYTHONPATH) && pytest test -vvv

security-check: install-requirements
	source venv/bin/activate && bandit src/lambda_func.py src/upload_data_file.py src/delete_data_file.py src/run_upload_data_file.py src/run_delete_data_file.py && pip-audit -r ./requirements.txt

check-pep8-compliance: install-requirements
	source venv/bin/activate && flake8 src test

run-checks: unit-test security-check check-pep8-compliance

uninstall-requirements: create-environment
	source venv/bin/activate && $(PIP) uninstall -r requirements.txt
