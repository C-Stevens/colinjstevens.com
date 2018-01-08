#!/bin/bash
verify_success() {
	if [ $1 != 0 ]; then 
		echo "$2";
		exit 1
	fi
}

install() {
	INSTALL_DIR=$(pwd)
	export BASE_DIR=$INSTALL_DIR
	ln -s $INSTALL_DIR/res $INSTALL_DIR/blog/assets/borrow
	verify_success $? "Unable to create asset symlink"
	make
	verify_success $? "Site building was unsuccessful"
	unset BASE_DIR
	echo "Install successful."
	echo "-----------------"
	echo "NOTE: BASE_DIR must be manually set to $INSTALL_DIR (or whatever you choose) for future building!"
	echo "-----------------"
}

install
exit 0
