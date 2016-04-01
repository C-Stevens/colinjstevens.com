#
# Makefile for colinjstevens.com
# (c) Colin Stevens 2016, refer to LICENSE file
# for licensing information.
#
# Depends:
#	python3 (https://python.org)
#

BASE_DIR ?= /home/web/www/colinjstevens.com
SRC_DIR = $(BASE_DIR)/src
BUILD_DIR = $(BASE_DIR)/build

all: clean git-init build
stage: clean build # TODO: Change base dir

build: build-init index
	cp $(BUILD_DIR)/index.html $(BASE_DIR)

git-init:
	git pull

build-init:
	mkdir -p $(BUILD_DIR); \
	cp -r $(SRC_DIR)/* $(BUILD_DIR); \

index:
	python3 $(BUILD_DIR)/build.py $(BUILD_DIR)

clean:
	if [ -f "$(BASE_DIR)/index.html" ]; then rm "$(BASE_DIR)/index.html"; fi
	if [ -d "$(BUILD_DIR)" ]; then rm -rf "$(BUILD_DIR)"; fi
