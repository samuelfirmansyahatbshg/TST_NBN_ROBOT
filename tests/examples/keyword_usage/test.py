"""
COPYRIGHT © BSH HOME APPLIANCES GROUP  2023

ALLE RECHTE VORBEHALTEN. ALL RIGHTS RESERVED.

The reproduction, transmission or use of this document or its contents is not permitted without express
written authority. Offenders will be liable for damages. All rights, including rights created by  patent
grant or registration of a utility model or design, are reserved.
"""
import pytest

from mason_base import Configuration
from mason_home_appliance.environment import HomeApplianceEnv

from configurations.test_object.config_builder import YourConstants


class Test:
    """
    This test class is a showcase for keyword usage in tests

    POSITIONS OF INTEREST:
    - tests/conftest.py::my_project fixture
    - configurations/test_object/config_builder.py
    """

    @pytest.mark.DeviceUnderTest(Configuration.PROJECTS.TST_PROJECT_NAME.GROUP_ALL)
    @pytest.mark.Status(Configuration.Status.RUNABLE)
    @pytest.mark.Intensity(Configuration.Intensity.SMOKE)
    @pytest.mark.TestType(Configuration.TestType.FUNCTIONAL)
    @pytest.mark.RequirementSource(Configuration.RequirementSource.DEMAND)
    def test_keywords_usage(self, ha_env: HomeApplianceEnv):
        """
        This tests demonstrates how to use the keywords from the mason-home-appliance-xyz layer.
        It powers the device, closes the door and starts a program with keywords implementation.
        It checks if the door is closed.

        :Requirements: write here the link to the requirements which is documented in polarion
        :Bugs: write here your link to polarion
        """
        ########################################################################
        # CONDITION
        ########################################################################
        # Bring up HomeAppliance in precondition
        ha_env.interaction.button.press(YourConstants.BUTTON_POWER)
        ########################################################################
        # ACTION
        ########################################################################
        # Door close
        ha_env.interaction.door.close(YourConstants.DOOR)
        # Start program
        ha_env.interaction.button.tap(YourConstants.BUTTON_START)
        ########################################################################
        # EXPECTATION
        ########################################################################
        # check if door is close
        assert ha_env.interaction.door.is_closed(YourConstants.DOOR)
