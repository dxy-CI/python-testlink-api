#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
@author: Kai Borowiak
@summary: TestSuite for testlink.objects.TestBuild
"""

# IMPORTS
import unittest
import inspect

from .. import randint, randput, randict

from testlink.objects import Build

class BuildTests(unittest.TestCase):

	def __init__(self,*args,**kwargs):
		super(BuildTests,self).__init__(*args,**kwargs)
		self._testMethodDoc = "Build: " + self._testMethodDoc

	def test__str__(self):
		"""String representation"""
		name = randput()
		obj = Build(name=name)
		string = str(obj)
		self.assertEqual(string, "Build: %s" % name)
