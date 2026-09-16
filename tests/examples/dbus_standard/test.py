"""
COPYRIGHT © BSH HOME APPLIANCES GROUP 2023

ALLE RECHTE VORBEHALTEN. ALL RIGHTS RESERVED.

The reproduction, transmission or use of this document or its contents is not permitted without express
written authority. Offenders will be liable for damages. All rights, including rights created by  patent
grant or registration of a utility model or design, are reserved.
"""
import pytest
import time

from mason_base import Configuration


class Test:
    """This class contains a collection of tests regarding the feature"""

    @pytest.mark.DeviceUnderTest(Configuration.PROJECTS.TST_PROJECT_NAME.GROUP_ALL)
    @pytest.mark.Status(Configuration.Status.RUNABLE)
    @pytest.mark.Intensity(Configuration.Intensity.SMOKE)
    @pytest.mark.TestType(Configuration.TestType.FUNCTIONAL)
    @pytest.mark.RequirementSource(Configuration.RequirementSource.DEMAND)
    def test_dbus_standard(self, env, init_dbus):
        """
        This tests demonstrates to send a message with the dbus module from mason base. It sends a message which is
        includes in the Messages.json file in the configurations/components/dbus folder.
        This message will ask the SMM for his IP-address.

        :Requirements: - `PROJECT-1234 <https://production.polarion.bshg.com/link-to-req-PROJECT-1234>`_
                       - `PROJECT-1235 <https://production.polarion.bshg.com/link-to-req-PROJECT-1235>`_
        :Bugs: - `ISSUE-0815 <https://issuetracking.bsh-sdd.com/link-to-ISSUE-0815>`_
               - `ISSUE-0816 <https://issuetracking.bsh-sdd.com/link-to-ISSUE-0816>`_
        """

        ########################################################################
        # CONDITION
        ########################################################################
        # reset all old dbus messages in queue
        env.dbus.reset()
        ########################################################################
        # ACTION
        ########################################################################
        # send test msg to communication partner
        env.dbus.send("TEST_MSG_SMM_IPv4_ADDRESS_REQ", [0x1])
        # wait to assure the message is processed at the communication partner side
        time.sleep(0.5)
        ########################################################################
        # EXPECTATION
        ########################################################################
        # ask if the response message is shown on the dbus
        assert env.dbus.get_dbusmsg_obj("TEST_MSG_SMM_IPv4_ADDRESS_RESP")
