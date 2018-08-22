#!/usr/bin/env python
# encoding: utf-8

from setuptools import setup, find_packages

setup(
	name = 'duplicates',
	version = '1.0',
	description = 'Duplicates search and removal. The wrapper over duplicate-file-finder',
	author = 'Alexey Mavrin',
	author_email = 'alexeymavrin@gmail.com',
	platforms = ['mac', 'linux', 'windows'],
	packages = find_packages(),	 # automatically add packages
	package_dir = {'duplicates': 'duplicates'}, # where the package in source tree
	package_data = {'duplicates':['non-pack-deps/duplicate-file-finder/*']},
	include_package_data = True,
	license = 'MIT License',
	# install_requires = [],
	# dependency_links = ['https://github.com/michaelkrisper/duplicate-file-finder'],
	entry_points = {
		'console_scripts': [
		  'duplicates = duplicates.duplicates:main',
		]
	  }
)

