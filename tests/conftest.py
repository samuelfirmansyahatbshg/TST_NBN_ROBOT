"""
COPYRIGHT © BSH HOME APPLIANCES GROUP 2023

ALLE RECHTE VORBEHALTEN. ALL RIGHTS RESERVED.

The reproduction, transmission or use of this document or its contents is not permitted without express
written authority. Offenders will be liable for damages. All rights, including rights created by patent
grant or registration of a utility model or design, are reserved.
"""
import pytest

from configurations.test_object.config_builder import ProjectConfigModel
from mason_base.environment import ENV
from mason_home_appliance.environment import HomeApplianceEnv
from mason_home_appliance.ha_env_configurator.configurator.ha_env_configurator import HAEnvConfigurator


@pytest.fixture(scope="session", autouse=False)
def my_project(env: ENV, ha_env: HomeApplianceEnv, init_wago):
    """
    If keyword is used, set the fixture to autouse as True or create a dependency to this. Fixture ha_env should be
    replaced  with your domain specific env fixture like ha_env_cl for cooling. The names of these fixtures can be found
    here: https://pages.github-bshg.boschdevcloud.com/DEV-TST-TOOLS/mason-home-appliance/Build/Tester/KeywordDrivenTesting/get_started.html#domain-specific-environment-fixtures
    """
    # Insert Objects creation here
    config_model = ProjectConfigModel().create_config_model()

    # Do the configuration
    configurator: HAEnvConfigurator = HAEnvConfigurator(ha_env)
    configurator.configure(config_model)
    return ha_env
