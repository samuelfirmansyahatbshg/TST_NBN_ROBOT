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
from coords import Coords
from mason_base import configuration
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
    @pytest.mark.DeviceUnderTest(configuration.PROJECTS.TST_PROJECT_NAME.GROUP_ALL)
    def test_demo(self, env, init_robot):
        """
        apply coords, read camera
        """

        logging.bsh_step_logger.info("test_request_response")
        env.dbus.reset()
        # env.dbus.send("RESET_IABO", [0x01])

        env.image_source.setup_image_source()
        image_source = ImageAcquisitionFactory.get_image_source()

        env.robot.initialize()
        move_named_position(Positions.ON_OFF)
        move_named_position(Positions.ON_OFF_DOWN)
        move_named_position(Positions.ON_OFF)
        move_named_position(Positions.CAM)
        # sleep(0.5)
        txt = "thermador"
        img = image_source.capture(1, 10000)["images"][0]
        image_source._save_image(img, f"./results/{txt}.jpg")
        sleep(4.0)

        img = image_source.capture(1, 10000)["images"][0]
        print(Text.retrieve_roi_center(img, "Convection Bake",
                                       {
                                           "boldness": 0,
                                           "size": 35
                                       }, "None"))
        txt = "default"
        image_source._save_image(img, f"./results/{txt}.jpg")
        move_named_position(Positions.LIGHT)
        move_named_position(Positions.LIGHT_DOWN)
        move_named_position(Positions.LIGHT)
        move_named_position(Positions.MIDDLE)
        move_named_position(Positions.MIDDLE_DOWN)
        move_named_position(Positions.MIDDLE_SWIPE)
        move_named_position(Positions.MIDDLE_SWIPE_UP)
        move_named_position(Positions.CAM)
        img = image_source.capture(1, 10000)["images"][0]
        print(Text.retrieve_roi_center(img, "Bake",
                                       {
                                           "boldness": 0,
                                           "size": 35
                                       }, "None"))
        txt = "bake_mode"
        image_source._save_image(img, f"./results/{txt}.jpg")
        move_named_position(Positions.START_UP)
        move_named_position(Positions.START_DOWN)
        move_named_position(Positions.START_UP)
        move_named_position(Positions.CAM)
        img = image_source.capture(1, 10000)["images"][0]
        txt = "bake_started"
        image_source._save_image(img, f"./results/{txt}.jpg")
        move_named_position(Positions.LIGHT)
        move_named_position(Positions.LIGHT_DOWN)
        move_named_position(Positions.LIGHT)

        move_named_position(Positions.START_UP)
        move_named_position(Positions.START_DOWN)
        move_named_position(Positions.START_UP)

        for i in range(3):
            move_named_position(Positions.LONG_SWIPE)
            move_named_position(Positions.LONG_SWIPE_DOWN)
            move_named_position(Positions.LONG_SWIPE_END)
            move_named_position(Positions.LONG_SWIPE_END_UP)

        move_named_position(Positions.MIDDLE)
        move_named_position(Positions.MIDDLE_DOWN)
        move_named_position(Positions.MIDDLE_SWIPE)
        move_named_position(Positions.MIDDLE_SWIPE_UP)

        move_named_position(Positions.START_UP)
        move_named_position(Positions.START_DOWN)
        move_named_position(Positions.START_UP)
        move_named_position(Positions.CAM)
        img = image_source.capture(1, 10000)["images"][0]
        print(Text.retrieve_roi_center(img, "Rotisserie",
                                       {
                                           "boldness": 0,
                                           "size": 35
                                       }, "None"))
        txt = "Rotisserie"
        image_source._save_image(img, f"./results/{txt}.jpg")

        move_named_position(Positions.ON_OFF)
        move_named_position(Positions.ON_OFF_DOWN)
        move_named_position(Positions.ON_OFF)

        move_named_position(Positions.HOME)

        sleep(2.0)
        env.dbus.send("RESET_CPM", [0x01])
        env.dbus.send("RESET_IABO", [0x01])
