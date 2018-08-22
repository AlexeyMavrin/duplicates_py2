"""
Created on Jan 23, 2018

@author: alexeymavrin@gmail.com

"""

import sys
reload(sys)
sys.setdefaultencoding('utf8')  # make sure we handle unicode

import os
import unittest
import shutil
from StringIO import StringIO

sys.path.append(os.path.abspath(".."))  # test module from the parent directory
import duplicates.duplicates as duplicates
# import time

class PhotosHandlerE2EValidation(unittest.TestCase):

	def setUp(self):
		# save stdout to a variable
		self.stdout_orig = sys.stdout
		self.stdout = StringIO()
		sys.stdout = self.stdout
		self.argv = sys.argv  # preserve arguments

		# copy sample to tst
		shutil.rmtree("unsorted", ignore_errors = True)
		shutil.rmtree("tgt", ignore_errors = True)
		shutil.rmtree("tst", ignore_errors = True)
		shutil.copytree("sample", "tst")

	def tearDown(self):
		sys.stdout = self.stdout_orig
		sys.argv = self.argv  # restore arguments
		# print self.stdout.getvalue().strip()

		# clear tst
		shutil.rmtree("unsorted", ignore_errors = True)
		shutil.rmtree("tst")
		shutil.rmtree("tgt", ignore_errors = True)
		shutil.rmtree("tst copy", ignore_errors = True)


	def test_straight(self):
		'''test that duplicates.py finds all the duplicates in the sample folder'''

		sys.argv = ['-v', '-g', os.path.join('tst', 'golden'), '-w', os.path.join('tst', 'work'), '--purge']

		all_files = duplicates.get_all_files("tst")
		self.assertEqual(16, len(all_files), "total files")
		# print len(all_files), all_files

		# 1. find all duplicates
		# with self.assertRaises(duplicates.GreatSuccess):
			# duplicates.main()
		duplicates.main()

		all_files = duplicates.get_all_files("tst")
		self.assertEqual(8, len(all_files), "total files")

		all_files = duplicates.get_all_files("tst/work")
		# print len(all_files), all_files
		self.assertEqual(1, len(all_files), "total files")

		all_files = duplicates.get_all_files("tst/golden")
		# print len(all_files), all_files
		self.assertEqual(5, len(all_files), "total files")


	def test_reverse(self):
		'''to make sure that the golden would not change - test wise versa'''

		sys.argv = ['-v', '-w', os.path.join('tst', 'golden'), '-g', os.path.join('tst', 'work'), "-p"]

		all_files = duplicates.get_all_files("tst")
		self.assertEqual(16, len(all_files), "total files")
		# print len(all_files), all_files

		all_files = duplicates.get_all_files("tst/work")
		self.assertEqual(9, len(all_files), "total files")
		# print len(all_files), all_files

		# 1. find all duplicates
		# with self.assertRaises(duplicates.GreatSuccess):
			# duplicates.main()
		duplicates.main()

		all_files = duplicates.get_all_files("tst")
		self.assertEqual(12, len(all_files), "total files")

		all_files = duplicates.get_all_files("tst/work")
		# print len(all_files), all_files
		self.assertEqual(9, len(all_files), "total files")

		all_files = duplicates.get_all_files("tst/golden")
		# print len(all_files), all_files
		self.assertEqual(1, len(all_files), "total files")


	def test_path(self):
		'''what if work is in golden'''

		sys.argv = ['-v', '-g', os.path.join('tst', ''), '-w', os.path.join('tst', 'work')]

		all_files = duplicates.get_all_files("tst")
		self.assertEqual(16, len(all_files), "total files")

		# find all duplicates
		with self.assertRaises(duplicates.ArgumentCheck):
			duplicates.main()

		all_files = duplicates.get_all_files("tst")
		self.assertEqual(16, len(all_files), "total files")


	def test_path_same(self):
		'''what if work is in golden (same path)'''

		sys.argv = ['-v', '-g', os.path.join('tst', ''), '-w', os.path.join('tst', '')]

		all_files = duplicates.get_all_files("tst")
		self.assertEqual(16, len(all_files), "total files")

		# find all duplicates
		with self.assertRaises(duplicates.ArgumentCheck):
			duplicates.main()

		all_files = duplicates.get_all_files("tst")
		self.assertEqual(16, len(all_files), "total files")


	def test_path2(self):
		'''what if golden is in work'''

		sys.argv = ['-v', '-w', os.path.join('tst', ''), '-g', os.path.join('tst', 'golden'), "-p"]

		all_files = duplicates.get_all_files("tst")
		self.assertEqual(16, len(all_files), "total files before")

		# find all duplicates
		# with self.assertRaises(duplicates.GreatSuccess):
			# duplicates.main()
		duplicates.main()

		all_files = duplicates.get_all_files("tst")
		self.assertEqual(7, len(all_files), "total files after")

		all_files = duplicates.get_all_files("tst/work")
		self.assertEqual(1, len(all_files), "files in work")

		all_files = duplicates.get_all_files("tst/golden")
		self.assertEqual(5, len(all_files), "files in work")


	def test_date1(self):
		'''make sure we preserve the oldest'''

		sys.argv = ['-v', '-w', os.path.join('tst', ''), '-g', os.path.join('tst', 'golden'), '-p']

		# change modify time
		tfn = 'tst/work/1/.new.jpg'
		self.assertTrue(os.path.isfile(tfn), '%s eists' % (tfn))
		# mtime = os.path.getmtime(tfn)
		# print mtime
		os.utime(tfn, (0, 0))
		# os.path.getmtime('tst/golden/duplicate copy.jpg')

		# find all duplicates
		# with self.assertRaises(duplicates.GreatSuccess):
			# duplicates.main()
		duplicates.main()

		self.assertTrue(os.path.isfile(tfn), '%s eists' % (tfn))

		all_files = duplicates.get_all_files("tst")
		self.assertEqual(7, len(all_files), "total files after")


	def test_date2(self):
		'''make sure to remove most recent'''

		sys.argv = ['-v', '-w', os.path.join('tst', ''), '-g', os.path.join('tst', 'golden'), "-p"]

		# change modify time
		tfn = 'tst/work/1/.new.jpg'
		self.assertTrue(os.path.isfile(tfn), '%s eists' % (tfn))
		mtime = os.path.getmtime(tfn)
		# print mtime
		os.utime(tfn, (mtime * 2, mtime * 2))
		# os.path.getmtime('tst/golden/duplicate copy.jpg')

		# with self.assertRaises(duplicates.GreatSuccess):
			# duplicates.main()
		duplicates.main()

		self.assertFalse(os.path.isfile(tfn), '%s eists' % (tfn))

		all_files = duplicates.get_all_files("tst")
		self.assertEqual(7, len(all_files), "total files after")


	def test_no_golden(self):
		'''make sure we keep one good version in work if golden is not given'''

		sys.argv = ['-v', '-w', os.path.join('tst', ''), "-p"]

		all_files = duplicates.get_all_files("tst")
		self.assertEqual(16, len(all_files), "total files")

		# 1. find all duplicates
		# with self.assertRaises(duplicates.GreatSuccess):
			# duplicates.main()
		duplicates.main()

		all_files = duplicates.get_all_files("tst")
		self.assertEqual(6, len(all_files), "total files")


	def test_duplicates_similar_names(self):
		'''similar names'''

		sys.argv = ['-v', '-w', os.path.join('tst copy', ''), '-g', os.path.join('tst', ''), "-p"]

		shutil.rmtree("tst copy", ignore_errors = True)
		shutil.copytree("sample", "tst copy",)

		all_files = duplicates.get_all_files("tst")
		self.assertEqual(16, len(all_files), "total files")
		all_files = duplicates.get_all_files("tst copy")
		self.assertEqual(16, len(all_files), "total files")

		duplicates.main()

		all_files = duplicates.get_all_files("tst")
		self.assertEqual(16, len(all_files), "total files")

		all_files = duplicates.get_all_files("tst copy")
		self.assertEqual(0, len(all_files), "total files")


	def test_duplicates_similar_names2(self):
		'''similar names the other way around'''

		sys.argv = ['-v', '-g', os.path.join('tst copy', ''), '-w', os.path.join('tst', ''), "-p"]

		shutil.rmtree("tst copy", ignore_errors = True)
		shutil.copytree("sample", "tst copy",)

		all_files = duplicates.get_all_files("tst")
		self.assertEqual(16, len(all_files), "total files")
		all_files = duplicates.get_all_files("tst copy")
		self.assertEqual(16, len(all_files), "total files")

		duplicates.main()

		all_files = duplicates.get_all_files("tst")
		self.assertEqual(0, len(all_files), "total files")

		all_files = duplicates.get_all_files("tst copy")
		self.assertEqual(16, len(all_files), "total files")


if __name__ == '__main__':
	unittest.main()
	"""
	suite = unittest.TestSuite()
	suite.addTest(PhotosHandlerE2EValidation("test_duplicates_similar_names2"))
	runner = unittest.TextTestRunner()
	runner.run(suite)
	# """
