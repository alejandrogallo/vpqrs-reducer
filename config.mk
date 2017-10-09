PYTHON = python3
PIP = pip3
TEST_COMMAND = $(PYTHON) -m doctest vpqrsreducer/*.py ; \
							 $(PYTHON) -m pytest vpqrsreducer


.PHONY: cc4s-real

scripts/vpqrsreducer:
	(cd scripts/ ; ln -s ../vpqrsreducer/ .)

cc4s-real: scripts/vpqrsreducer ## Create real integrals for cc4s
	$(PYTHON) scripts/cc4s-real.py

