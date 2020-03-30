# create by afterloe
# version is 1.0
# MIT License

.PHONY: build,dist,test,zip

PATH := /home/pi/.local/bin:$(PATH)
SHELL := /bin/bash
PROJECT_NAME := talk_to_me

# CI指令
all: test build zip

test: tests
	@pytest

build: main.spec
	@pyinstaller main.spec

.ONESHELL:
zip: dist
	cd dist;
	mv main $(PROJECT_NAME)
	zip -q -r -m -o $(PROJECT_NAME).zip $(PROJECT_NAME);
	mv $(PROJECT_NAME).zip ..
	cd ..
	rm -rf dist build

.ONESHELL:
install: $(PROJECT_NAME).zip
	sudo rm -rf /usr/local/$(PROJECT_NAME)
	sudo mv $(PROJECT_NAME).zip /usr/local
	cd /usr/local
	sudo unzip $(PROJECT_NAME).zip
	sudo rm -rf $(PROJECT_NAME).zip
	cd ${PROJECT_NAME}
	./main -v