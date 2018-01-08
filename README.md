# Introduction
This repository holds all the relevant to my [personal website](https://colinjstevens.com).

# Assets Used
This project makes use of a few assets to make things look slick and run well, most of which are listed below:
* [Semantic UI](http://semantic-ui.com)
* [jQuery](https://jquery.com/)
* [Subtle Patterns](http://subtlepatterns.com)
* [Fira Sans](https://github.com/mozilla/Fira)
* [nginx](http://nginx.com/)
* [jekyll](https://jekyllrb.com/)

# Quickstart
The site can be built and deployed very easily, with only minor modifications before building. See below for a quick guide to get the site running (sans the webserver configuration file).
### Pull the base files and change directory
```shell
$ git clone --recursive https://github.com/C-Stevens/colinjstevens.com.git /destination/dir
$ cd /destination/dir
$ ./setup.sh
```
### Edit the Makefile
The makefile must be edited and `BASE_DIR` set explicitly to the new destination directory. Otherwise, the makefile will set `BASE_DIR` to `/home/web/www/colinjstevens.com` by default, and the site may not build properly in the future after initial setup.

## Developing
Included in the repository is [`stage-make.sh`](/stage-make.sh). This script allows easier development by specifying a different `BASE_DIR` and `JEKYLL_ARGS` before making the site with the `stage` target (this target will omit pulling recent changes from the remote repository).

While developing, your dev directory can be set in this file (as well as any additional jekyll arguments, e.g `--drafts`) to avoid accidentally building the production site set in the Makefile's `BASE_DIR`.

Since the `stage` target of the Makefile does not pull from the remote repository but the production target does, changes can be made, commited, and pushed to the repo so that when the production site is built normally all changes from development are included (**So don't push anything before testing!**)

Additionally, the `stage-make.sh` file allows arbitrary commands to be run under development environment variables with the `-i` flag to enter interactive mode. This allows any other command can be run under the same environment expected when using the script regurally (e.g to execute  `$ make clean` without cleaning the production directory).

The production site can be built as easily as executing:
```shell
$ make
```
in the source directory of the site, provided you have set `BASE_DIR` to the correct production directory after running the setup script.

# License
For detailed licensing information, refer to the [license](/LICENSE.md) file.

# Todo
* Minifify source files in src/ in build.py
