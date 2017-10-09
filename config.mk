PYTHON = python3
PIP = pip3
TEST_COMMAND = $(PYTHON) -m doctest vpqrsreducer/*.py ; \
							 $(PYTHON) -m pytest vpqrsreducer

