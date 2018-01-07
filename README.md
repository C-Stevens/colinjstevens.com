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
## Pull the base files and change directory
```shell
$ git clone --recursive https://github.com/C-Stevens/colinjstevens.com.git /destination/dir
$ cd /destination/dir
```
## Edit the makefile
The makefile needs to be edited to update only the `BASE_DIR` value. In this case, it would be set to destination/dir

## Create asset symblink for the blog
This is necessary for the blog subfolder to access resouces used by the main site
```shell
$ ln -s /full/path/to/destination/dir/res /full/path/to/destination/dir/blog/assets/borrow
```
## Build the site
```shell
$ make
```

# License
For detailed licensing information, refer to the [license](/LICENSE.md) file.

# Todo
* Minifify source files in src/ in build.py
