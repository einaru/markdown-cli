
CLEANDIRS = build dist mdcli.egg-info

.PHONY: install build clean

install:
	python setup.py install

build:
	python setup.py sdist

clean:
	rm -rf $(CLEANDIRS)
