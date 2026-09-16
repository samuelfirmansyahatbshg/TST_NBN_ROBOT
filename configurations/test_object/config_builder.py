"""
COPYRIGHT © BSH HOME APPLIANCES GROUP  2023

ALLE RECHTE VORBEHALTEN. ALL RIGHTS RESERVED.

The reproduction, transmission or use of this document or its contents is not permitted without express
written authority. Offenders will be liable for damages. All rights, including rights created by  patent
grant or registration of a utility model or design, are reserved.
"""
from dataclasses import dataclass

from mason_home_appliance.ha_env_configurator.configuration_model.test_object_element import TestObjectElement
from mason_home_appliance.ha_env_configurator.configuration_model.ha_env_configuration_model import \
    HAEnvConfigurationModel
from mason_home_appliance.interaction import ButtonFactory
from mason_home_appliance.interaction.door.door_factory import DoorFactory


@dataclass
class YourConstants:
    """
    Name constants for config and test usage
    """
    DOOR = "DOOR"
    BUTTON_START = "BUTTON_START"
    BUTTON_POWER = "BUTTON_POWER"


class ProjectConfigModel:
    """
    Class for creating the configuration model. Keywords and their implementations are defined here.
    """
    # This class can be renamed based on the product such as OvenConfigModel.

    def __init__(self):
        """
        Initialize standard implementations.
        If needed you can in addition append more objects to your config_model later.
        """
        # Create multiple object of a Keyword button
        self.button_elements = TestObjectElement()
        self.button_elements.keyword = "interaction.button"
        self.button_elements.factory_type = ButtonFactory
        self.button_elements.name = [YourConstants.BUTTON_START, YourConstants.BUTTON_POWER]
        self.button_elements.implementation = "BUTTON_TCB"  # or use the full path to the implementation class
        self.button_elements.properties = [
            {'port': 'K1'},
            {'port': 'K2'}]

        # Create an object of keyword door
        self.door_elements = TestObjectElement()
        self.door_elements.keyword = "interaction.door"
        self.door_elements.factory_type = DoorFactory
        self.door_elements.name = YourConstants.DOOR
        self.door_elements.implementation = "DOOR_WAGO"  # or use the full path to the implementation class
        self.door_elements.properties = {'port': 'DO_S0'}

    def create_config_model(self) -> HAEnvConfigurationModel:
        """
        Creates the config model and returns with all added elements to your test environment.
        """
        # Build configuration model
        config_model: HAEnvConfigurationModel = HAEnvConfigurationModel()
        config_model.test_object_elements.append(self.door_elements)
        config_model.test_object_elements.append(self.button_elements)

        return config_model
