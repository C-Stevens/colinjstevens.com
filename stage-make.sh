export BASE_DIR=/home/web/www/cjs-stage && \
export JEKYLL_ARGS="--incremental --drafts --config _config.yml,_config-dev.yml" && \

make -e stage ; \

unset -v JEKYLL_ARGS
unset -v BASE_DIR
