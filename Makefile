VIRTUALENV ?= /usr/bin/virtualenv
# The Python binary to use when running the virtualenv script. Also used for
# running the tests when TEST_PYTHON isn't provided.
PYTHON ?= python
NOSE ?= nosetests
VIRTUALENV_DIR ?= $(error VIRTUALENV_DIR must be set when running virtualenv or ci-tests targets)
# The Python binary to use when running tests.
TEST_PYTHON ?= $(PYTHON)
PYTHONPATH ?= vendor/lib/python
# A pip requirements file describing the dependencies that should be installed
# into the virtualenv.
REQUIREMENTS=requirements/dev.txt
COMPILED_REQUIREMENTS=requirements/compiled.txt

ifdef VERBOSE
NOSE_ARGS=-v
TEST_ARGS=-v
endif

ALL_PY_FILES := $(shell find . -iname "*.py")

# Used to run the tests. Useful for both CI-driven tests and manual ones.
test: test.done
test.done: $(ALL_PY_FILES)
	@echo Running unit tests
	PYTHONPATH=$(PYTHONPATH) $(NOSE) $(NOSE_ARGS)
	@echo Running rules tests
	$(TEST_PYTHON) test-rules.py $(TEST_ARGS)
	touch $@

# Creates a virtualenv containing all the requirements needed to run tests.
virtualenv:
	$(PYTHON) $(VIRTUALENV) --no-site-packages $(VIRTUALENV_DIR)
	$(VIRTUALENV_DIR)/bin/pip -q install -r $(REQUIREMENTS)
	$(VIRTUALENV_DIR)/bin/pip -q install -r $(COMPILED_REQUIREMENTS)

clobber-test:
	$(RM) test.done

# Run the tests, installing any necessary libraries into a virtualenv.
ci-tests: NOSE=$(VIRTUALENV_DIR)/bin/nosetests
ci-tests: TEST_PYTHON=$(VIRTUALENV_DIR)/bin/python
ci-tests: clobber-test virtualenv test
