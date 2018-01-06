export BASE_DIR=/home/web/www/cjs-stage && \
export JEKYLL_ARGS="--drafts" && \

if [ -n "$1" ] && [ "$1" == "-i" ]; then
	echo -n ">>> " ; read cmd
	eval $cmd
else
	make -e stage
fi

unset -v JEKYLL_ARGS
unset -v BASE_DIR
