#!/usr/bin/env python
# pylint: disable=line-too-long
# pylint: disable=invalid-name
# pylint: disable=star-args
# pylint: disable=too-many-locals
# pylint: disable=too-many-arguments

"""Requirement Object"""

# IMPORTS
import datetime

from testlink.objects.tl_object import TestlinkObject
from testlink.objects.tl_object import normalize_list
from testlink.objects.tl_object import _STRPTIME_FUNC as strptime

from testlink.objects.tl_risk import Risk

from testlink.enums import REQ_TYPE as RequirementType
from testlink.enums import REQ_STATUS as RequirementStatus

# pylint: disable=too-many-instance-attributes
class Requirement(TestlinkObject):
    """Testlink Requirement representation"""

    __slots__ = ("srs_id", "req_doc_id", "req_spec_title", "typ", "version", "version_id", "revision", "revision_id",\
            "scope", "status", "node_order", "is_open", "active", "expected_coverage", "testproject_id", "author",\
            "author_id", "creation_ts", "modifier", "modifier_id", "modification_ts", "_parent_testproject")

    def __init__(\
            self,\
            srs_id=None,\
            req_doc_id='',\
            title='',\
            req_spec_title=None,\
            typ=RequirementType.INFO,\
            version=-1,\
            version_id=-1,\
            revision=-1,\
            revision_id=-1,\
            scope='',\
            status=RequirementStatus.DRAFT,\
            node_order=0,\
            is_open="1",\
            active="1",\
            expected_coverage=1,\
            testproject_id=-1,\
            author=None,\
            author_id=-1,\
            creation_ts=str(datetime.datetime.min),\
            modifier=None,\
            modifier_id=-1,\
            modification_ts=str(datetime.datetime.min),\
            api=None,\
            parent_testproject=None,\
            **kwargs\
    ):
        """Initializes a new Requirement with the specified parameters
        @todo: doc
        """
        TestlinkObject.__init__(self, kwargs.get('id'), title, api)
        self.srs_id = str(srs_id)
        self.req_doc_id = str(req_doc_id)
        self.req_spec_title = req_spec_title
        self.typ = int(typ)
        self.version = int(version)
        self.version_id = int(version_id)
        self.revision = int(revision)
        self.revision_id = int(revision_id)
        self.scope = scope
        self.status = str(status)
        self.node_order = int(node_order)
        self.is_open = bool(int(is_open))
        self.active = bool(int(active))
        self.expected_coverage = int(expected_coverage)
        self.testproject_id = int(testproject_id)
        self.author = str(author)
        self.author_id = int(author_id)
        self.modifier = str(modifier)
        try:
            self.modifier_id = int(modifier_id)
        except ValueError:
            self.modifier_id = -1
        try:
            self.creation_ts = strptime(str(creation_ts), TestlinkObject.DATETIME_FORMAT)
        except ValueError:
            self.creation_ts = datetime.datetime.min
        try:
            self.modification_ts = strptime(str(modification_ts), TestlinkObject.DATETIME_FORMAT)
        except ValueError:
            self.modification_ts = datetime.datetime.min
        self._parent_testproject = parent_testproject

    def __str__(self):
        return "Requirement %s: %s" % (self.req_doc_id, self.name)

    def getTestProject(self):
        """Returns the associated TestProject"
        @returns: TestProject
        @rtype: TestProject
        """
        return self._parent_testproject

    def iterRisk(self, name=None, **params):
        """Returns all Risks with the specified parameters.
        @param name: The name of the wanted Risk
        @type name: str
        @returns: Matching Risks
        @rtype: generator
        """
        # No simple API call, so get all Risks for the current Requirement
        response = self._api.getRisksForRequirement(self.id)
        risks = [Risk(api=self._api, parent_testproject=self.getTestProject(), **risk) for risk in response]

        # Filter
        if len(params) > 0 or name:
            params['name'] = name
            for rk in risks:
                for key, value in params.items():
                    # Skip None
                    if value is None:
                        continue
                    try:
                        if not unicode(getattr(rk, key)) == unicode(value):
                            rk = None
                            break
                    except AttributeError:
                        raise AttributeError("Invalid Search Parameter for Risk: %s" % key)
                # Return found risk
                if rk is not None:
                    yield rk
        # Return all found risks
        else:
            for rk in risks:
                yield rk

    def getRisk(self, name=None, **params):
        """Returns all Risks with the specified parameters
        @param name: The name of the Risk
        @type name: str
        @returns: Matching Risks
        @rtype: mixed
        """
        return normalize_list([r for r in self.iterRisk(name, **params)])
