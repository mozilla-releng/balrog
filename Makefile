test:
	@echo Running unit tests
	nosetests
	@echo Running rule tests
	python test-rules.py
