VIRTUALENV ?= /usr/bin/virtualenv
COVERAGE_BIN ?= coverage
# The Python binary to use when running the virtualenv script.
PYTHON ?= python
NOSE ?= $(shell which nosetests)
# When COVERAGE is set, python code coverage reports will be generated
# during test runs.
COVERAGE ?=
VIRTUALENV_DIR ?= $(error VIRTUALENV_DIR must be set when running virtualenv or ci-tests targets)
PYTHONPATH ?= vendor/lib/python
# A pip requirements file describing the dependencies that should be installed
# into the virtualenv.
REQUIREMENTS = requirements/dev.txt
COMPILED_REQUIREMENTS = requirements/compiled.txt

ifdef VERBOSE
NOSE_ARGS += -v
TEST_ARGS += -v
endif

# Append the test directory to the nose args, to avoid picking up files like
# auslib/util/testing.py.
NOSE_ARGS += auslib/test

ALL_PY_FILES := $(shell find . -iname "*.py")

PYTHON_ENV = PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=$(PYTHONPATH)
# Used to run the tests. Useful for both CI-driven tests and manual ones.
test: test.done
test.done: $(ALL_PY_FILES) $(if $(ALWAYS_RUN_TESTS), FORCE)
	@echo Running unit tests
ifdef COVERAGE
	$(RM) -r .coverage htmlcov
	-$(PYTHON_ENV) $(COVERAGE_BIN) run $(NOSE) $(NOSE_ARGS)
else
	-$(PYTHON_ENV) $(NOSE) $(NOSE_ARGS)
endif
	@echo Running rules tests
ifdef COVERAGE
	-$(COVERAGE_BIN) run -a test-rules.py $(TEST_ARGS)
	$(COVERAGE_BIN) html --include='*auslib*'
else
	-$(PYTHON) test-rules.py $(TEST_ARGS)
endif
	touch $@

# Creates a virtualenv containing all the requirements needed to run tests.
PIP_INSTALL = $(VIRTUALENV_DIR)/bin/pip -q install
virtualenv:
	$(PYTHON) $(VIRTUALENV) --no-site-packages $(VIRTUALENV_DIR)
	$(PIP_INSTALL) -r $(REQUIREMENTS)
	$(PIP_INSTALL) -r $(COMPILED_REQUIREMENTS)

test-in-virtualenv: PYTHON=$(VIRTUALENV_DIR)/bin/python
test-in-virtualenv: NOSE=$(VIRTUALENV_DIR)/bin/nosetests
test-in-virtualenv: COVERAGE_BIN=$(VIRTUALENV_DIR)/bin/coverage
test-in-virtualenv: test

# Run the tests, installing any necessary libraries into a virtualenv.
ci-tests: virtualenv test-in-virtualenv

.PHONY: FORCE
