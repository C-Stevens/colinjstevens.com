#!/bin/bash
export BASE_DIR=/home/web/www/cjs-stage && \
export JEKYLL_ARGS="--drafts" && \
echo "Successfully loaded development env"

if [ "$1" == "-i" ]; then
	echo -n ">>> " ; read cmd
	eval $cmd
else
	make -e stage
fi

unset -v JEKYLL_ARGS
unset -v BASE_DIR
