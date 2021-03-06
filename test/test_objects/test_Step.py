#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
@author: Kai Borowiak
@summary: TestCase for testlink.objects.TestCase.Step
"""

# IMPORTS
import unittest

from .. import randput, randint

from testlink.objects.tl_step import Step

class StepTests(unittest.TestCase):
    """Step Object Tests"""

    def __init__(self, *args, **kwargs):
        super(StepTests, self).__init__(*args, **kwargs)
        self._testMethodDoc = "TestCase.Step: " + self._testMethodDoc

    def test__str__(self):
        """String representation"""
        number = randint()
        actions = randput()
        results = randput()

        obj = Step(step_number=number, actions=actions, expected_results=results)
        string = str(obj)
        self.assertEqual(string, "Step %d:\n%s\n%s" % (number, actions, results))
