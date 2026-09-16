"""
COPYRIGHT © BSH HOME APPLIANCES GROUP  2023

ALLE RECHTE VORBEHALTEN. ALL RIGHTS RESERVED.

The reproduction, transmission or use of this document or its contents is not permitted without express
written authority. Offenders will be liable for damages. All rights, including rights created by  patent
grant or registration of a utility model or design, are reserved.
"""
import pytest

from mason_base import Configuration

# For the testproject an own logging source name is defined in __init__.py.
# This makes it easier to separate between Mason, Mason HA or testing project as logging source
from tests import logger


class Test:
    """This class contains a collection of tests regarding logging with mason"""

    @pytest.mark.DeviceUnderTest(Configuration.PROJECTS.TST_PROJECT_NAME.GROUP_ALL)
    @pytest.mark.Status(Configuration.Status.RUNABLE)
    @pytest.mark.Intensity(Configuration.Intensity.SMOKE)
    @pytest.mark.TestType(Configuration.TestType.FUNCTIONAL)
    @pytest.mark.RequirementSource(Configuration.RequirementSource.DEMAND)
    def test_logger_showcase(self, env):
        """
        This test will show the logging in mason.
        for further documentation please have a look into the following link:

        :Documentation: - `Mason Logger Documentation <https://pages.github-bshg.boschdevcloud.com/DEV-TST-TOOLS/mason-base/Build/Developer/Logging/Mason_logger.html>`_
        :Requirements: write here the link to the requirements which is documented in polarion
        :Bugs: write here your link to polarion
        """

        ########################################################################
        # CONDITION
        ########################################################################
        value = 42
        ########################################################################
        # ACTION
        ########################################################################
        # prints the value and also logs it into result file
        logger.info(f"logging number of value: {value}")
        ########################################################################
        # EXPECTATION
        ########################################################################
        assert True
