"""
COPYRIGHT © BSH HOME APPLIANCES GROUP  2023

ALLE RECHTE VORBEHALTEN. ALL RIGHTS RESERVED.

The reproduction, transmission or use of this document or its contents is not permitted without express
written authority. Offenders will be liable for damages. All rights, including rights created by  patent
grant or registration of a utility model or design, are reserved.
"""

import pytest

from mason_base import Configuration


class TestMarkerHandlingDemo(object):
    @pytest.mark.DeviceUnderTest(Configuration.PROJECTS.TST_PROJECT_NAME.GROUP_ALL)
    @pytest.mark.Status(Configuration.Status.RUNABLE)
    @pytest.mark.Intensity(Configuration.Intensity.SMOKE)
    @pytest.mark.TestType(Configuration.TestType.FUNCTIONAL)
    @pytest.mark.RequirementSource(Configuration.RequirementSource.DEMAND)
    def test_marker_handling_1(self, env, init_robot):
        """
        This test verifies ...
        This test is data driven with the following data sets: ...

        :Requirements: - `PROJECT-1234 <https://production.polarion.bshg.com/link-to-req-PROJECT-1234>`_
                       - `PROJECT-1235 <https://production.polarion.bshg.com/link-to-req-PROJECT-1235>`_
        :Bugs: - `ISSUE-0815 <https://issuetracking.bsh-sdd.com/link-to-ISSUE-0815>`_
               - `ISSUE-0816 <https://issuetracking.bsh-sdd.com/link-to-ISSUE-0816>`_
        """
        env.robot.initialize()
        env.robot.move_absolute(10.00, 10.00, 5.00, int(100), True)
        env.robot.move_absolute(200.00, 80.00, 5.00, int(100), True)
        for i in range(100):
            txt = input("Give coord (x.0,y.0)")
            lst = txt.split(',')
            env.robot.move_absolute(float(lst[0]), float(lst[1]), 5.00, int(100), True)

        ########################################################################
        # CONDITION
        ########################################################################
        pass            # dummy for setting the condition (GIVEN)
        ########################################################################
        # ACTION
        ########################################################################
        pass            # dummy for setting the action (WHEN)
        ########################################################################
        # EXPECTATION
        ########################################################################
        a = 8           # dummy for getting some value from anywhere
        assert a < 9    # and finally verify the expectation (THEN)

