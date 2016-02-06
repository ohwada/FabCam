#!/usr/bin/env python
# coding=utf-8

__author__ = "Kenichi Ohwada"

from setuptools import setup, find_packages
import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(os.path.realpath(__file__)), "src"))
import fabcam_setuptools

#-----------------------------------------------------------------------------------------------------------------------

# Requirements for our application
INSTALL_REQUIRES = [
	"tornado==4.0.1",
	"pyserial==2.7",
]

# Additional requirements for setup
SETUP_REQUIRES = []

# Dependency links for any of the aforementioned dependencies
DEPENDENCY_LINKS = []

# Additional requirements for optional install options
EXTRA_REQUIRES = dict()

# general setup configuration
def params():
	name = "FabCam"
	version = "0.1"

	description = "FabCam tool for Raspberry Pi"

	install_requires = INSTALL_REQUIRES
	extras_require = EXTRA_REQUIRES
	dependency_links = DEPENDENCY_LINKS
	setup_requires = SETUP_REQUIRES

	classifiers = [
		"Development Status :: 0.1 - Beta",
		"Environment :: Web Environment",
		"Intended Audience :: Education",
		"Intended Audience :: End Users/Desktop",
		"Intended Audience :: Manufacturing",
		"Intended Audience :: Science/Research",
		"License :: OSI Approved :: Modified BSD License",
		"Natural Language :: English",
		"Operating System :: OS Independent",
		"Programming Language :: Python :: 2.7",
		"Programming Language :: JavaScript",
		"Topic :: Internet :: WWW/HTTP",
		"Topic :: Internet :: WWW/HTTP :: Dynamic Content",
		"Topic :: Internet :: WWW/HTTP :: WSGI",
		"Topic :: Printing",
		"Topic :: System :: Networking :: Monitoring"
	]

	author = "Kenichi Ohwada"
	author_email = "web.ohwada@gmail.com"
	url = "http://ohwada.jp/"
	license = "Modified BSD License"

	packages = find_packages("src")
	package_dir = {
		"":"src"
	}
	package_data = {
		"fabcam": fabcam_setuptools.package_data_dirs('src/fabcam', ['static', 'templates', 'conf'])
	}

	include_package_data = True
	zip_safe = False

	if os.environ.get('READTHEDOCS', None) == 'True':
		# we can't tell read the docs to please perform a pip install -e .[develop], so we help
		# it a bit here by explicitly adding the development dependencies, which include our
		# documentation dependencies
		install_requires = install_requires + extras_require['develop']

	entry_points = {
		"console_scripts": [
			"fabcam = fabcam:main"
		]
	}

	return locals()

setup(**params())
