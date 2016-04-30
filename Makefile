#
# Makefile for colinjstevens.com
# (c) Colin Stevens 2016, refer to LICENSE file
# for licensing information.
#
# Depends:
#	python3 (https://python.org)
#

BUILD_DATE := $(shell date | sed 's/ /-/g')

BASE_DIR ?= /home/web/www/colinjstevens.com
SRC_DIR = $(BASE_DIR)/src
BUILD_DIR = $(BASE_DIR)/build
BUILD_HISTORY_DIR = $(BASE_DIR)/build-history

all: clean git-init build
stage: clean build

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
	if [ -d "$(BUILD_DIR)" ]; then cp -r $(BUILD_DIR) $(BUILD_HISTORY_DIR)/$(BUILD_DATE); rm -rf "$(BUILD_DIR)"; fi
