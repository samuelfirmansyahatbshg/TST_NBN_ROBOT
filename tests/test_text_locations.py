"""
COPYRIGHT © BSH HOME APPLIANCES GROUP  2023

ALLE RECHTE VORBEHALTEN. ALL RIGHTS RESERVED.

The reproduction, transmission or use of this document or its contents is not permitted without express
written authority. Offenders will be liable for damages. All rights, including rights created by  patent
grant or registration of a utility model or design, are reserved.
"""

import os
import sys
import pytest
from mason_base.Core.image_acquisition.image_acquisition_factory import ImageAcquisitionFactory
# always check that Image Source has been configured
from mason_base.Core.image_acquisition.image_acquisition_interface import ImageAcquisitionInterface
import tests.example_images.rois as ROI
from mason_base import Configuration
from mason_base.Core.vision.image_filter.image_filter import ContrastSwapTypeEnum
from mason_base.Core.vision.presentation.text import Text
# from utilities.reconfigure_mason import reconfigure_mason_modules as reconfigure


@pytest.mark.Intensity(Configuration.Intensity.SMOKE)
@pytest.mark.DeviceUnderTest(Configuration.PROJECTS.TST_PROJECT_NAME.GROUP_ALL)
class TestVisionTextLocalizer:

    def setup_class(self):
        # reconfigure(r'tests/mason_config.ini')
        folder = r"tests/example_images"
        self.img_folder_path = os.path.join(*folder.split('/'))

    # @pytest.mark.skip("Only for local testing and playing")
    def test_text_single_line(self):
        img = r"tests/example_images/temp_12.png"
        args = {}
        args["size"] = 55
        args["boldness"] = 0.5
        Text.verify(img, {
            ROI.TEMP_1_SCOLAGEMENTO: "Scongelamento pane bianco"
        }, args)

    def test_roi_localizer_conv(self):
        img = r"tests/example_images/default.jpg"
        print(Text.retrieve_roi_center(img, "Convection Bake",
                                 {
                                     "boldness": 0,
                                     "size": 35
                                 },"None"))

    def test_roi_localizer(self):
        img = r"tests/example_images/temp_12.png"
        Text.retrieve_roi_center(img, "Scongelamento pane bianco",
                                 {
                                     "boldness": 0,
                                     "size": 55
                                 },
                                 "None")



    @pytest.mark.parametrize(
        'data',
        [
            ("temp_11", "Defrost white bread")
        ])
    def test_roi_localizer_full(self, data):
        img = os.path.join(self.img_folder_path, data[0]) + ".png"
        center = Text.retrieve_roi_center(img, data[1],
                                          {
                                              "boldness": 0.5,
                                              "size": 55,
                                              "debug": 0
                                          })
        if center is not None:
            pass
        else:
            raise AssertionError("Roi was not found")

    def test_text_single_line2(self):
        img = r"tests/example_images/temp_22.png"
        Text.verify(img, {
            ROI.TEMP_2_SECOND_FULL: "Bake savory\nfresh cooked\ningredients"
        },
                    {
                        "boldness": 0.5,
                        "size": 55,
                        "filter_contrast_swap_method": ContrastSwapTypeEnum.advanced_histogram,
                        # "debug_log": BirdDebugLevels.FULL,
                        # "debug_log_target": "web_browser"
                    })

    def test_text_single_line3(self):
        img = r"tests/example_images/temp_22.png"
        Text.verify(img, {
            ROI.TEMP_2_THIRD_FULL: "Potato gratin,\nraw ingredients"
        },
                    {
                        "boldness": 0.5,
                        "size": 55,
                        "filter_contrast_swap_method": ContrastSwapTypeEnum.advanced_histogram,
                        # "debug_log": BirdDebugLevels.FULL,
                        # "debug_log_target": "web_browser"
                    })

    def test_text_single_line_another_image(self):
        img = r"tests/example_images/temp_21.png"
        Text.verify(img, {
            ROI.TEMP_2_FIRST_FULL: "Pavlova"
        },
                    {
                        "boldness": 0.5,
                        "size": 55,
                        "filter_contrast_swap_method": ContrastSwapTypeEnum.advanced_histogram,
                        "debug": 0
                        # "debug_log": BirdDebugLevels.FULL,
                        # "debug_log_target": "web_browser"
                    })

