"""
COPYRIGHT © BSH HOME APPLIANCES GROUP  2023

ALLE RECHTE VORBEHALTEN. ALL RIGHTS RESERVED.

The reproduction, transmission or use of this document or its contents is not permitted without express
written authority. Offenders will be liable for damages. All rights, including rights created by  patent
grant or registration of a utility model or design, are reserved.
"""

import pytest

from mason_base import Configuration

from mason_base.Core.image_acquisition.image_acquisition_factory import ImageAcquisitionFactory
# always check that Image Source has been configured
from mason_base.Core.image_acquisition.image_acquisition_interface import ImageAcquisitionInterface

class TestCam(object):
    @pytest.mark.DeviceUnderTest(Configuration.PROJECTS.TST_PROJECT_NAME.GROUP_ALL)
    def test_cam(self, env):
        env.image_source.setup_image_source()
        if Configuration.Equipment.match(Configuration.Equipment._IMAGE_SOURCE):
            # get reference to image source instance e. g. the Basler Camera
            image_source = ImageAcquisitionFactory.get_image_source()
            # create a image, function returns a list of images
            images = image_source.capture(1, 30000)
            first_image = images[ImageAcquisitionInterface.KEY_IMAGES][0]
            # save image
            image_source._save_image(first_image, "./vision/my_image.jpg")

