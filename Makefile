typehint:
	mypy --ignore-missing-imports app.py

lint:
	pylint app.py

checklist: lint typehint 

black:
	black -l 79 app.py

setup:
	$(VIRTUAL_ENV)/bin/pip install -r requirements-unittest.txt

.PHONY: typehint lint checklist black