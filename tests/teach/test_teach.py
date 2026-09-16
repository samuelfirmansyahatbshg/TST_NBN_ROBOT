"""
COPYRIGHT © BSH HOME APPLIANCES GROUP  2023

ALLE RECHTE VORBEHALTEN. ALL RIGHTS RESERVED.

The reproduction, transmission or use of this document or its contents is not permitted without express
written authority. Offenders will be liable for damages. All rights, including rights created by  patent
grant or registration of a utility model or design, are reserved.
"""

import pytest
import logging
from time import sleep
from mason_base import Configuration
from mason_base.Core.image_acquisition.image_acquisition_factory import ImageAcquisitionFactory
from mason_base.Core.image_acquisition.image_acquisition_interface import ImageAcquisitionInterface
from mason_base.environment import ENV
from mason_base.Core.dbus_bsh.dbus_base.decoder_base import BshDBusMsg
from fixtures.uda_fixtures import FixtureNamesUDA
from mason_base.fixtures.dbus_bsh_fixtures import init_dbus
from mason_base.Core.vision.presentation.text import Text


def move_named_position(position):
    ENV().robot.move_absolute(position[0], position[1], position[2], int(100), True)


class Positions:

    CAM = [292.0, 70.0, 20.0]
    ON_OFF = [159.10, 159.50, 20.00]
    ON_OFF_DOWN = [159.10, 159.50, 47.00]
    LIGHT = [196.3, 159.50, 20.00]
    TIMERS = [234.20, 159.50, 20.00]
    FAST = [308.30, 159.50, 20.00]
    INFO = [346.40, 159.50, 20.00]
    DRAWER = [384.60, 159.50, 20.0]
    UPPER_CAV = [358.00, 118.00, 20.00]
    UPPER_CAV_TAP = [358.00, 118.00, 47.00]
    LOWER_CAV = [352.00, 135.00, 20.00]
    LOWER_CAV_TAP = [352.00, 135.00, 47.00]

    LIGHT_DOWN = [196.3, 159.50, 47.00]
    MIDDLE = [292.00, 120.0, 20.00]
    MIDDLE_DOWN = [292.00, 120.0, 47.00]
    MIDDLE_SWIPE = [270.00, 120.0, 47.00]
    MIDDLE_SWIPE_UP = [270.00, 120.0, 20.00]
    START_UP = [422.70, 159.50, 20.00]
    START_DOWN = [422.70, 159.50, 47.00]
    LONG_SWIPE = [320.00, 120.0, 20.00]
    LONG_SWIPE_DOWN = [320.00, 120.0, 47.00]
    LONG_SWIPE_END = [270.00, 120.0, 47.00]
    LONG_SWIPE_END_UP = [270.00, 120.0, 20.00]
    HOME = [5.00, 5.0, 5.00]

class TestMarkerHandlingDemo(object):
    @pytest.mark.usefixtures(FixtureNamesUDA.DBUS_TIMING)
    @pytest.mark.usefixtures(init_dbus.__name__)
    @pytest.mark.DeviceUnderTest(Configuration.PROJECTS.TST_PROJECT_NAME.GROUP_ALL)
    def test_demo(self, env, init_robot):
        """
        apply coords, read camera
        """

        logging.bsh_step_logger.info("test_request_response")
        env.robot.initialize()
        for i in range(20):
            move_named_position(Positions.UPPER_CAV)
            move_named_position(Positions.UPPER_CAV_TAP)
            move_named_position(Positions.UPPER_CAV)
            move_named_position(Positions.LOWER_CAV)
            move_named_position(Positions.LOWER_CAV_TAP)
            move_named_position(Positions.LOWER_CAV)

        while True:
            str_pos = input("Give pos in")
            if str_pos == "q":
                ENV().robot.move_absolute(5.0, 5.0, 5.0, int(100), True)
                break
            if str_pos is not "":
                try:
                    pos1, pos2, pos3 = str_pos.split(",")
                    ENV().robot.move_absolute(float(pos1), float(pos2), float(pos3), int(100), True)
                except ValueError:
                    print("Wrong input")



