PYTHON = python3
PIP = pip3
TEST_COMMAND = $(PYTHON) -m doctest vpqrsreducer/*.py ; \
							 $(PYTHON) -m pytest vpqrsreducer


.PHONY: cc4s-real

out:
	mkdir out

scripts/vpqrsreducer:
	(cd scripts/ ; ln -s ../vpqrsreducer/ .)

## <<HELP
#
#                            Scripts that can be run
#
## HELP

cc4s-real: out scripts/vpqrsreducer ## Create real integrals for cc4s
	$(PYTHON) scripts/$@.py | tee out/$@.out
	$(SED) -n '/if .*/,$$ p' out/$@.out > out/$@.cpp

cc4s-complex: out scripts/vpqrsreducer ## Create complex integrals for cc4s
	$(PYTHON) scripts/$@.py | tee out/$@.out
	$(SED) -n '/if .*/,$$ p' out/$@.out > out/$@.cpp
