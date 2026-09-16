"""
        COPYRIGHT © BSH HOME APPLIANCES GROUP  2019  GED

        ALLE RECHTE VORBEHALTEN. ALL RIGHTS RESERVED.

        The reproduction, transmission or use of this document or its contents is not permitted without express
        written authority. Offenders will be liable for damages. All rights, including rights created by  patent
        grant or registration of a utility model or design, are reserved.

        Name: uda_fixtures.py

        Created on 27.11.2020 in TST_mason-acceptance-tests
"""
import pytest
import logging
import os
import platform
from aenum import Constant
from pyUda import DBusMode, PyUda
import time


@pytest.fixture(scope="class")
def init_dbus_timing(request):
    """
    Init dbus timing for different platforms

    :param request: request fixture to get information about current test
    """
    if(platform.system() == 'Windows'):
        request.cls.dbus_delay = 0.25
        request.cls.id_string_timeout = 10
    else:
        machine = os.uname().machine
        logging.bsh_step_logger.info(f"Detected machine: {machine}")
        if(machine == "x86_64"):
            request.cls.dbus_delay = 0.25
            request.cls.id_string_timeout = 10
        else:
            request.cls.dbus_delay = 0.5
            request.cls.id_string_timeout = 20

    logging.bsh_step_logger.info(f"Init Dbus Timing: dbus_delay: {request.cls.dbus_delay} - "
                                 f"id_string_timeout: {request.cls.id_string_timeout}")


@pytest.fixture(scope="function")
def uda_stim(request, env, init_dbus):
    """
    :brief: Initialize stimulation uda.
    """
    wait_time_connect_uda: int = 10

    # Get uda not used for testing
    version: int = None
    uda_id: int = None
    if env.dbus.uda_properties['uda_type'] == 'UDA2':
        version = 1
        uda_id = 1
    else:
        version = 2
    timeout = time.time() + wait_time_connect_uda
    while time.time() < timeout:
        try:
            env.uda_stim = PyUda(version, uda_id)
            break
        except Exception as e:
            logging.bsh_step_logger.warning(f"The following exception got from PyUda: {e} ")
            time.sleep(1)
    env.uda_stim.setDBusMode(DBusMode.DBus2)
    env.uda_stim.setBaudrate(9600)
    env.uda_stim.setSimulatedDevices(0x0, 0x5)
    env.uda_stim.setSendRetry(0)

    def fin():
        env.uda_stim.closeConnection()
        env.uda_stim = None


    request.addfinalizer(fin)


@pytest.fixture(scope="session")
def init_second_dbus(request, env):
    """
    :brief: Method to connect to the DBUS of the tested home appliance on a session level,
    which prevents the Setup and Teardown being done for every single testfunction. Instead it is done only once.
    """
    if env.first_dbus:
        env.first_dbus.setup_dbus_bsh()

    if env.second_dbus:
        env.second_dbus.setup_dbus_bsh()

        def fin():
            """
            Finalizer for bsh dbus module
            """
            env.first_dbus.delete_bsh_dbus()
            env.second_dbus.delete_bsh_dbus()
            env.first_dbus = None
            env.second_dbus = None
        request.addfinalizer(fin)


@pytest.fixture(scope="session")
def init_mcu_second_uda(request, env):
    """
    :brief: Method to connect to the DBUS of the tested home appliance on a session level,
    which prevents the Setup and Teardown being done for every single testfunction. Instead it is done only once.
    """
    if hasattr(env, "second_dbus") and env.mcu:
        env.second_dbus.setup_dbus_bsh()
        env.mcu.setup_mcu()

        def fin():
            """
            Finalizer for bsh dbus module
            """
            env.second_dbus.delete_bsh_dbus()
        request.addfinalizer(fin)


class FixtureNamesUDA(Constant):
    """
    UDA fixture function names
    """
    STIM_UDA = uda_stim.__name__
    SECOND_DBUS = init_second_dbus.__name__
    MCU_SECOND_UDA = init_mcu_second_uda.__name__
    DBUS_TIMING = init_dbus_timing.__name__
