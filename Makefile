SHELL := /usr/bin/bash
APPDIR := ./AppDir
APPDIR_APPLICATION := ${APPDIR}/opt/application
GLIBC_VERSION := $(shell getconf GNU_LIBC_VERSION | sed 's/ /-/g' )
PWD := $(shell pwd)

all: init appimage clean

init:
	rm -rf $(PWD)/venv
	python3 -m venv --copies $(PWD)/venv
	source $(PWD)/venv/bin/activate && python3 -m pip install -r $(PWD)/requirements.txt


appimage: clean
	rm -rf ${APPDIR}/venv
	cp -r ./venv ${APPDIR}
	rm -rf $(APPDIR_APPLICATION)
	mkdir -p $(APPDIR_APPLICATION)
	cp -r ./src/charts $(APPDIR_APPLICATION)
	cp -r ./src/icons $(APPDIR_APPLICATION)
	cp -r ./src/lib $(APPDIR_APPLICATION)
	cp -r ./src/modules $(APPDIR_APPLICATION)
	cp -r ./src/plugins $(APPDIR_APPLICATION)
	cp -r ./src/templates $(APPDIR_APPLICATION)
	cp -r ./src/themes $(APPDIR_APPLICATION)
	cp ./src/main.py $(APPDIR_APPLICATION)
	bin/appimagetool-x86_64.AppImage  ./AppDir bin/AOD-PerformanceTuner.AppImage
	@echo "done: bin/AOD-PerformanceTuner.AppImage"

clean:
	rm -rf ${APPDIR}/venv
	rm -rf ${APPDIR}/opt
