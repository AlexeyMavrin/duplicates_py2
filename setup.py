#!/usr/bin/env python
# encoding: utf-8

from __future__ import print_function
import setuptools
from setuptools.command.install import install
from setuptools.command.test import test
import subprocess
import os

class TestCommand(test, object):

	def run(self):
		# run the unit test to make sure that there is no regression
		import test.test_e2e as e2e_test
		e2e_test.main()

class InstallCommand(install, object):
	"""Get dependencies from github before install"""

	def initialize_options(self):
		"""clone duplicate-file-finder before install"""
		# get latest from https://github.com/michaelkrisper/duplicate-file-finder.git
		print("Getting duplicate file finder from https://github.com/michaelkrisper/duplicate-file-finder.git")
		path = os.path.abspath(os.path.join(os.path.dirname(os.path.realpath(__file__)), "duplicates", "non-pack-deps"))

		subprocess.call(r"git clone https://github.com/michaelkrisper/duplicate-file-finder.git",
							shell = True,
							cwd = path)
		subprocess.check_call(r"git pull",
							shell = True,
							cwd = os.path.join(path, "duplicate-file-finder"))

		# run install
		# install.run(self)
		super(InstallCommand, self).initialize_options()


setuptools.setup(
	cmdclass = {'install': InstallCommand, 'test': TestCommand},
	name = 'duplicates',
	version = '1.0',
	description = 'Duplicates search and removal. The wrapper over duplicate-file-finder',
	author = 'Alexey Mavrin',
	author_email = 'alexeymavrin@gmail.com',
	platforms = ['mac', 'linux', 'windows'],
	packages = setuptools.find_packages(),  # automatically add packages
	package_dir = {'duplicates': 'duplicates'}, # where the package in source tree
	package_data = {'duplicates':['non-pack-deps/duplicate-file-finder/*']},
	include_package_data = True,
	install_requires = ['humanize', ],
	license = 'MIT License',
	# dependency_links = ['https://github.com/michaelkrisper/duplicate-file-finder'],
	entry_points = {
		'console_scripts': [
		  'duplicates = duplicates.duplicates:main',
		]
	  }
)

