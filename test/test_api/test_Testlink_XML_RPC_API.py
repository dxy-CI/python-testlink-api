#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
@author: Kai Borowiak
@summary: TestSuite for testlink.api.Testlink_XML_RPC_API
"""

# IMPORTS
import unittest
from mock import Mock, MagicMock, patch
import string
import random

from testlink.api import Testlink_XML_RPC_API
from testlink.exceptions import *

from distutils.version import LooseVersion as Version
import threading
import SimpleXMLRPCServer
import xmlrpclib

import logging
#logging.basicConfig(level=logging.DEBUG)

def input(length=10):
	"""Generates random input with specified length
	@param length: Length of input (Default: 10)
	@type length: int
	@returns: Randomly generated string
	@rtype:str
	"""
	return ''.join(random.choice(string.ascii_uppercase + string.ascii_lowercase + string.digits) for _ in range(length))

def randict(*args):
	"""Genrates a dictionary with random values.
	@param args: Keys of the resulting dict
	@type args: list
	@returns: Dictionary with *args as keys and random values
	@rtype: dict
	"""
	res = {}
	for arg in args:
		res[arg] = input()
	return res
	

class Testlink_XML_RPC_API_Tests(unittest.TestCase):

	def setUp(self):
		"""Needed to connect to a mocked Server endpoint in each test"""
		self._patcher = patch('xmlrpclib.ServerProxy',spec=True)
		self._mock_server = self._patcher.start()
		self._api = Testlink_XML_RPC_API("http://localhost/lib/api/xmlrpc.php")
		self._api._proxy = self._mock_server

	def tearDown(self):
		self._patcher.stop()

	# We need to patch to the 'real' ServerProxy here to get good results
	def test_invalid_url(self):
		self.assertRaises(Exception,Testlink_XML_RPC_API)
		self.assertRaises(ConnectionError,Testlink_XML_RPC_API,"SPAM")
		self.assertRaises(ConnectionError,Testlink_XML_RPC_API,"http://")
		self.assertRaises(ConnectionError,Testlink_XML_RPC_API,"http://127.0.0.1/")
		self.assertRaises(ConnectionError,Testlink_XML_RPC_API,"http://127.0.0.1/lib/api/")

	def test_query(self):
		# Define mock endpoints
		self._mock_server.passed = Mock(return_value="SPAM!")
		self._mock_server.error = Mock(return_value=[{'code':1337,'message':'SPAM!'}])

		# Check endpoints
		self.assertEqual(self._api._query("passed"),"SPAM!")
		self.assertRaises(APIError,self._api._query,"error")

		# Check APIError struct
		try:
			self._api._query("error")
		except APIError,ae:
			self.assertEquals(ae.errorCode,1337)
			self.assertEquals(ae.errorString,"SPAM!")

		# Check correct variable forwarding
		data = randict("a","b","c")
		self._api._query("passed",**data)
		self._mock_server.passed.assert_called_with(dict(a=data['a'],b=data['b'],c=data['c'],devKey=None))

		# Check global devkey setting
		data = randict("a","b","c")
		key = input()
		self._api._devkey = key
		self._api._query("passed",**data)
		self._mock_server.passed.assert_called_with(dict(a=data['a'],b=data['b'],c=data['c'],devKey=key))

	#
	# The following tests have all the same structure:
	#
	# @patch("testlink.api.Testlink_XML_RPC_API._query")
	# def test_foo(self,query):
	#
	#     # Mock already query result
	#     query.return_value = input()
	#
	#     # Check if version check succeeds
	#     self.assertRaises(NotSupported,self._api.foo,*args,**kwargs)
	#
	#     # Patch Testlink Version if needed to get pass the TLVersion decorator (OPTIONAL)
	#     self._api._tl_version = Version("x.x.x")
	#
	#     # Verify result and matches with query result
	#     # Also verify passed arguments
	#     self.assertEquals(self._api.foo(), query.return_value)
	#     query.assert_called_with('foo',*args,**kwargs)
	#

	@patch("testlink.api.Testlink_XML_RPC_API._query")
	def test_testLinkVersion(self,query):
		query.return_value = "1.3.3.7"
		self.assertRaises(NotSupported,self._api.testLinkVersion)
		self._api._tl_version = Version("1.9.9")
		self.assertEquals(self._api.testLinkVersion(),"1.3.3.7")
		query.assert_called_with('tl.testLinkVersion')

	@patch("testlink.api.Testlink_XML_RPC_API._query")
	def test_about(self,query):
		query.return_value = input(50)
		self.assertEquals(self._api.about(),query.return_value)
		query.assert_called_with('tl.about')
		self._api._tl_version = Version("0.9")
		self.assertRaises(NotSupported,self._api.about)

	@patch("testlink.api.Testlink_XML_RPC_API._query")
	def test_sayHello(self,query):
		query.return_value = input()
		self.assertEquals(self._api.sayHello(),query.return_value)
		query.assert_called_with('tl.sayHello')
		self._api._tl_version = Version("0.9")
		self.assertRaises(NotSupported,self._api.sayHello)

	@patch("testlink.api.Testlink_XML_RPC_API._query")
	def test_repeat(self,query):
		query.return_value = input(20)
		test_data = query.return_value
		self.assertEquals(self._api.repeat(test_data),query.return_value)
		query.assert_called_with('tl.repeat',str=test_data)
		self._api._tl_version = Version("0.9")
		self.assertRaises(NotSupported,self._api.repeat)

	@patch("testlink.api.Testlink_XML_RPC_API._query")
	def test_checkDevKey(self,query):
		query.return_value = True
		test_data = input()
		self.assertEquals(self._api.checkDevKey(test_data),query.return_value)
		query.assert_called_with('tl.checkDevKey',devKey = test_data)
		self._api._tl_version = Version("0.9")
		self.assertRaises(NotSupported,self._api.checkDevKey)

	@patch("testlink.api.Testlink_XML_RPC_API._query")
	def test_doesUserExist(self,query):
		query.return_value = True
		test_data = input()
		self.assertEquals(self._api.doesUserExist(test_data),query.return_value)
		query.assert_called_with('tl.doesUserExist',user=test_data,devKey=None)
		self._api._tl_version = Version("0.9")
		self.assertRaises(NotSupported,self._api.doesUserExist)

	@patch("testlink.api.Testlink_XML_RPC_API._query")
	def test_getUserByLogin(self,query):
		query.return_value = input()
		test_data = input()
		self.assertRaises(NotSupported,self._api.getUserByLogin)
		self._api._tl_version = Version("1.9.8")
		self.assertEquals(self._api.getUserByLogin(test_data),query.return_value)
		query.assert_called_with('tl.getUserByLogin',user=test_data,devKey=None)

	@patch("testlink.api.Testlink_XML_RPC_API._query")
	def test_getUserByID(self,query):
		query.return_value = randict("name","id")
		test_data = input(2)
		self.assertRaises(NotSupported,self._api.getUserByID)
		self._api._tl_version = Version("1.9.8")
		self.assertEquals(self._api.getUserByID(test_data),query.return_value)
		query.assert_called_with('tl.getUserByID',userid=test_data,devKey=None)

	@patch("testlink.api.Testlink_XML_RPC_API._query")
	def test_getFullPath(self,query):
		query.return_value = input()
		test_data = input()
		self.assertEquals(self._api.getFullPath(test_data),query.return_value)
		query.assert_called_with('tl.getFullPath',nodeID=test_data,devKey=None)
		self._api._tl_version = Version("0.9")
		self.assertRaises(NotSupported,self._api.getFullPath)

	@patch("testlink.api.Testlink_XML_RPC_API._query")
	def test_createTestProject(self,query):
		query.return_value = randict("message")
		# Check default params
		defaults = randict("name","prefix")
		self.assertEquals(self._api.createTestProject(**defaults),query.return_value)
		query.assert_called_with('tl.createTestProject',\
							notes = '',\
							active = True,\
							public = True,\
							options = 	{'requirementsEnabled':False,\
									'testPriorityEnabled':False,\
									'automationEnabled':False,\
									'inventoryEnabled':False},\
							devKey = None,
							**defaults\
						)
		# Check with specified params
		options = randict("requirements","priority","automation","inventory")
		non_defaults = randict("name","prefix","notes","active","public")
		non_defaults.update(options)
		self.assertEquals(self._api.createTestProject(**non_defaults),query.return_value)
		query.assert_called_with('tl.createTestProject',\
							devKey = None,\
							options = 	{'requirementsEnabled':options['requirements'],\
									'testPriorityEnabled':options['priority'],\
									'automationEnabled':options['automation'],\
									'inventoryEnabled':options['inventory']},\
							name = non_defaults['name'],\
							prefix = non_defaults['prefix'],\
							notes = non_defaults['notes'],\
							active = non_defaults['active'],\
							public = non_defaults['public'],\
						)
		self._api._tl_version = Version("0.9")
		self.assertRaises(NotSupported,self._api.createTestProject)

	@patch("testlink.api.Testlink_XML_RPC_API._query")
	def test_getProjects(self,query):
		query.return_value = [randict("name")]
		self.assertEquals(self._api.getProjects(),query.return_value)
		query.assert_called_with('tl.getProjects',devKey = None)
		self._api._tl_version = Version("0.9")
		self.assertRaises(NotSupported,self._api.getProjects)

	@patch("testlink.api.Testlink_XML_RPC_API._query")
	def test_getTestProjectByName(self,query):
		test_data = randict("name")
		query.return_value = [test_data]
		self.assertEquals(self._api.getTestProjectByName(test_data['name']),query.return_value)
		query.assert_called_with('tl.getTestProjectByName',testprojectname=test_data['name'],devKey=None)
		self._api._tl_version = Version("0.9")
		self.assertRaises(NotSupported,self._api.getTestProjectByName)

	@patch("testlink.api.Testlink_XML_RPC_API._query")
	def test_createTestPlan(self,query):
		query.return_value = randict("message")
		# Check default params
		defaults = randict("name","project")
		self.assertEquals(self._api.createTestPlan(**defaults),query.return_value)
		query.assert_called_with('tl.createTestPlan',\
							notes = '',\
							active = True,\
							public = True,\
							devKey = None,\
							testplanname = defaults['name'],\
							testprojectname = defaults['project']\
						)
		# Check with specified params
		non_defaults = randict("name","project","notes","active","public")
		self.assertEquals(self._api.createTestPlan(**non_defaults),query.return_value)
		query.assert_called_with('tl.createTestPlan',\
							devKey = None,\
							active = non_defaults['active'],\
							public = non_defaults['public'],\
							notes = non_defaults['notes'],\
							testplanname = non_defaults['name'],\
							testprojectname = non_defaults['project']\
						)
		self._api._tl_version = Version("0.9")
		self.assertRaises(NotSupported,self._api.createTestPlan)

	@patch("testlink.api.Testlink_XML_RPC_API._query")
	def test_getTestPlanByName(self,query):
		test_data = randict("name","projectname")
		query.return_value = [test_data]
		self.assertEquals(self._api.getTestPlanByName(**test_data),query.return_value)
		query.assert_called_with('tl.getTestPlanByName',testplanname=test_data['name'],testprojectname=test_data['projectname'],devKey=None)
		self._api._tl_version = Version("0.9")
		self.assertRaises(NotSupported,self._api.getTestPlanByName)

	@patch("testlink.api.Testlink_XML_RPC_API._query")
	def test_getProjectTestPlans(self,query):
		test_data = input()
		query.return_value = [randict("name")]
		self.assertEquals(self._api.getProjectTestPlans(test_data),query.return_value)
		query.assert_called_with('tl.getProjectTestPlans',testprojectid=test_data,devKey=None)
		self._api._tl_version = Version("0.9")
		self.assertRaises(NotSupported,self._api.getProjectTestPlans)

	@patch("testlink.api.Testlink_XML_RPC_API._query")
	def test_getTestPlanCustomFieldValue(self,query):
		test_data = randict("testplanid","testprojectid","fieldname")
		query.return_value = input()
		self.assertRaises(NotSupported,self._api.getTestPlanCustomFieldValue)
		self._api._tl_version = Version("1.9.4")
		self.assertEquals(self._api.getTestPlanCustomFieldValue(**test_data),query.return_value)	
		query.assert_called_with('tl.getTestPlanCustomFieldValue',\
							devKey = None,\
							customfieldname = test_data['fieldname'],\
							testprojectid = test_data['testprojectid'],\
							testplanid = test_data['testplanid']\
						)
	
	@patch("testlink.api.Testlink_XML_RPC_API._query")
	def test_createBuild(self,query):
		query.return_value = randict("message")
		# Check default params
		defaults = randict("testplanid","name")
		self.assertEquals(self._api.createBuild(**defaults),query.return_value)
		query.assert_called_with('tl.createBuild',\
							devKey = None,\
							buildnotes = '',\
							buildname = defaults['name'],\
							testplanid = defaults['testplanid'],\
						)
		# Check with specified params
		non_defaults =randict("testplanid","name","notes")
		self.assertEquals(self._api.createBuild(**non_defaults),query.return_value)
		query.assert_called_with('tl.createBuild',\
							devKey = None,\
							buildnotes = non_defaults['notes'],\
							buildname = non_defaults['name'],\
							testplanid = non_defaults['testplanid']\
						)
		self._api._tl_version = Version("0.9")
		self.assertRaises(NotSupported,self._api.createBuild)

	@patch("testlink.api.Testlink_XML_RPC_API._query")
	def test_getLatestBuildForTestPlan(self,query):
		query.return_value = [randict("name","id")]
		test_data = input()
		self.assertEquals(self._api.getLatestBuildForTestPlan(test_data),query.return_value)
		query.assert_called_with('tl.getLatestBuildForTestPlan',devKey=None,testplanid=test_data)
		self._api._tl_version = Version("0.9")
		self.assertRaises(NotSupported,self._api.getLatestBuildForTestPlan)