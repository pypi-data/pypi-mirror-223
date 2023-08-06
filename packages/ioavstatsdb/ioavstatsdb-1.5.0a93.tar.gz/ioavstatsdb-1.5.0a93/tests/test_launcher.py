# Copyright (c) 2022 FAA-VAIL-Project. All rights reserved.
# Use of this source code is governed by the GNU LESSER GENERAL
# PUBLIC LICENSE, that can be found in the LICENSE.md file.

"""Launcher: coverage testing."""
import os
import platform

from ioavstatsdb import io_glob
from ioavstatsdb import io_utils
from ioavstatsdb.io_config import settings

# -----------------------------------------------------------------------------
# Constants & Globals.
# -----------------------------------------------------------------------------
# @pytest.mark.issue

EV_ID_1 = "20181022X64842"  # not US
EV_ID_2 = "20181212X03941"
EV_ID_3 = "20190401X25202"
EV_ID_4 = "20200908X83855"


# -----------------------------------------------------------------------------
# Test case: launcher() - version - Show the IO-AVSTATS-DB version.
# -----------------------------------------------------------------------------
# pylint: disable=R0801
def test_launcher_version():
    """Test case: launcher()."""
    # -------------------------------------------------------------------------
    io_glob.logger.debug(io_glob.LOGGER_START)

    assert settings.check_value == "test"

    if platform.system() == "Windows":
        os.system("run_io_avstats_pytest.bat version")
    elif platform.system() == "Linux":
        os.system("./run_io_avstats_pytest.sh version")
    else:
        # ERROR.00.908 The operating system '{os}' is not supported
        io_utils.terminate_fatal(
            io_glob.ERROR_00_908.replace("{os}", platform.system())
        )

    io_glob.logger.debug(io_glob.LOGGER_END)


# -----------------------------------------------------------------------------
# Test case: d_d_c   - Delete the PostgreSQL database container.
# -----------------------------------------------------------------------------
# pylint: disable=R0801
def test_launcher_d_d_c():
    """Test case: launcher()."""
    # -------------------------------------------------------------------------
    io_glob.logger.debug(io_glob.LOGGER_START)

    assert settings.check_value == "test"

    if platform.system() == "Windows":
        os.system("run_io_avstats_pytest.bat d_d_c")
    elif platform.system() == "Linux":
        os.system("./run_io_avstats_pytest.sh d_d_c")
    else:
        # ERROR.00.908 The operating system '{os}' is not supported
        io_utils.terminate_fatal(
            io_glob.ERROR_00_908.replace("{os}", platform.system())
        )

    io_glob.logger.debug(io_glob.LOGGER_END)


# -----------------------------------------------------------------------------
# Test case: d_d_f   - Delete the PostgreSQL database files.
# -----------------------------------------------------------------------------
# pylint: disable=R0801
def test_launcher_d_d_f():
    """Test case: launcher()."""
    # -------------------------------------------------------------------------
    io_glob.logger.debug(io_glob.LOGGER_START)

    assert settings.check_value == "test"

    if platform.system() == "Windows":
        os.system("run_io_avstats_pytest.bat d_d_f")
    elif platform.system() == "Linux":
        os.system("./run_io_avstats_pytest.sh d_d_f")
    else:
        # ERROR.00.908 The operating system '{os}' is not supported
        io_utils.terminate_fatal(
            io_glob.ERROR_00_908.replace("{os}", platform.system())
        )

    io_glob.logger.debug(io_glob.LOGGER_END)


# -----------------------------------------------------------------------------
# Test case: launcher() - s_d_c   - Set up the PostgreSQL database container.
# -----------------------------------------------------------------------------
# pylint: disable=R0801
def test_launcher_s_d_c():
    """Test case: launcher()."""
    # -------------------------------------------------------------------------
    io_glob.logger.debug(io_glob.LOGGER_START)

    assert settings.check_value == "test"

    if platform.system() == "Windows":
        os.system("run_io_avstats_pytest.bat s_d_c")
    elif platform.system() == "Linux":
        os.system("./run_io_avstats_pytest.sh s_d_c")
    else:
        # ERROR.00.908 The operating system '{os}' is not supported
        io_utils.terminate_fatal(
            io_glob.ERROR_00_908.replace("{os}", platform.system())
        )

    io_glob.logger.debug(io_glob.LOGGER_END)


# -----------------------------------------------------------------------------
# Test case: launcher() - c_d_s   - Create the PostgreSQL database schema.
# -----------------------------------------------------------------------------
# pylint: disable=R0801
def test_launcher_c_d_s():
    """Test case: launcher()."""
    # -------------------------------------------------------------------------
    io_glob.logger.debug(io_glob.LOGGER_START)

    assert settings.check_value == "test"

    if platform.system() == "Windows":
        os.system("run_io_avstats_pytest.bat c_d_s")
    elif platform.system() == "Linux":
        os.system("./run_io_avstats_pytest.sh c_d_s")
    else:
        # ERROR.00.908 The operating system '{os}' is not supported
        io_utils.terminate_fatal(
            io_glob.ERROR_00_908.replace("{os}", platform.system())
        )

    io_glob.logger.debug(io_glob.LOGGER_END)


# -----------------------------------------------------------------------------
# Test case: launcher() - u_d_s   - Update the PostgreSQL database schema.
# -----------------------------------------------------------------------------
# pylint: disable=R0801
def test_launcher_u_d_s():
    """Test case: launcher()."""
    # -------------------------------------------------------------------------
    io_glob.logger.debug(io_glob.LOGGER_START)

    assert settings.check_value == "test"

    if platform.system() == "Windows":
        os.system("run_io_avstats_pytest.bat u_d_s")
    elif platform.system() == "Linux":
        os.system("./run_io_avstats_pytest.sh u_d_s")
    else:
        # ERROR.00.908 The operating system '{os}' is not supported
        io_utils.terminate_fatal(
            io_glob.ERROR_00_908.replace("{os}", platform.system())
        )

    io_glob.logger.debug(io_glob.LOGGER_END)


# -----------------------------------------------------------------------------
# Test case: launcher() - a_o_c   - Load aviation occurrence categories
#                                   into PostgreSQL.
# -----------------------------------------------------------------------------
# pylint: disable=R0801
def test_launcher_a_o_c():
    """Test case: launcher()."""
    # -------------------------------------------------------------------------
    io_glob.logger.debug(io_glob.LOGGER_START)

    assert settings.check_value == "test"

    if platform.system() == "Windows":
        os.system("run_io_avstats_pytest.bat a_o_c")
    elif platform.system() == "Linux":
        os.system("./run_io_avstats_pytest.sh a_o_c")
    else:
        # ERROR.00.908 The operating system '{os}' is not supported
        io_utils.terminate_fatal(
            io_glob.ERROR_00_908.replace("{os}", platform.system())
        )

    io_glob.logger.debug(io_glob.LOGGER_END)


# -----------------------------------------------------------------------------
# Test case: launcher() - l_a_p   - Load airport data into PostgreSQL.
# -----------------------------------------------------------------------------
# pylint: disable=R0801
def test_launcher_l_a_p():
    """Test case: launcher()."""
    # -------------------------------------------------------------------------
    io_glob.logger.debug(io_glob.LOGGER_START)

    assert settings.check_value == "test"

    if platform.system() == "Windows":
        os.system("run_io_avstats_pytest.bat l_a_p")
    elif platform.system() == "Linux":
        os.system("./run_io_avstats_pytest.sh l_a_p")
    else:
        # ERROR.00.908 The operating system '{os}' is not supported
        io_utils.terminate_fatal(
            io_glob.ERROR_00_908.replace("{os}", platform.system())
        )

    io_glob.logger.debug(io_glob.LOGGER_END)


# -----------------------------------------------------------------------------
# Test case: launcher() - l_c_s   - Load country and state data into PostgreSQL.
# -----------------------------------------------------------------------------
# pylint: disable=R0801
def test_launcher_l_c_s():
    """Test case: launcher()."""
    # -------------------------------------------------------------------------
    io_glob.logger.debug(io_glob.LOGGER_START)

    assert settings.check_value == "test"

    if platform.system() == "Windows":
        os.system("run_io_avstats_pytest.bat l_c_s")
    elif platform.system() == "Linux":
        os.system("./run_io_avstats_pytest.sh l_c_s")
    else:
        # ERROR.00.908 The operating system '{os}' is not supported
        io_utils.terminate_fatal(
            io_glob.ERROR_00_908.replace("{os}", platform.system())
        )

    io_glob.logger.debug(io_glob.LOGGER_END)


# -----------------------------------------------------------------------------
# Test case: launcher() - l_s_e   - Load sequence of events data
#                                   into PostgreSQL.
# -----------------------------------------------------------------------------
# pylint: disable=R0801
def test_launcher_l_s_e():
    """Test case: launcher()."""
    # -------------------------------------------------------------------------
    io_glob.logger.debug(io_glob.LOGGER_START)

    assert settings.check_value == "test"

    if platform.system() == "Windows":
        os.system("run_io_avstats_pytest.bat l_s_e")
    elif platform.system() == "Linux":
        os.system("./run_io_avstats_pytest.sh l_s_e")
    else:
        # ERROR.00.908 The operating system '{os}' is not supported
        io_utils.terminate_fatal(
            io_glob.ERROR_00_908.replace("{os}", platform.system())
        )

    io_glob.logger.debug(io_glob.LOGGER_END)


# -----------------------------------------------------------------------------
# Test case: launcher() - l_s_d   - Load simplemaps data into PostgreSQL.
# -----------------------------------------------------------------------------
# pylint: disable=R0801
def test_launcher_l_s_d():
    """Test case: launcher()."""
    # -------------------------------------------------------------------------
    io_glob.logger.debug(io_glob.LOGGER_START)

    assert settings.check_value == "test"

    if platform.system() == "Windows":
        os.system("run_io_avstats_pytest.bat l_s_d")
    elif platform.system() == "Linux":
        os.system("./run_io_avstats_pytest.sh l_s_d")
    else:
        # ERROR.00.908 The operating system '{os}' is not supported
        io_utils.terminate_fatal(
            io_glob.ERROR_00_908.replace("{os}", platform.system())
        )

    io_glob.logger.debug(io_glob.LOGGER_END)


# -----------------------------------------------------------------------------
# Test case: launcher() - l_z_d   - Load ZIP Code Database data into PostgreSQL.
# -----------------------------------------------------------------------------
# pylint: disable=R0801
def test_launcher_l_z_d():
    """Test case: launcher()."""
    # -------------------------------------------------------------------------
    io_glob.logger.debug(io_glob.LOGGER_START)

    assert settings.check_value == "test"

    if platform.system() == "Windows":
        os.system("run_io_avstats_pytest.bat l_z_d")
    elif platform.system() == "Linux":
        os.system("./run_io_avstats_pytest.sh l_z_d")
    else:
        # ERROR.00.908 The operating system '{os}' is not supported
        io_utils.terminate_fatal(
            io_glob.ERROR_00_908.replace("{os}", platform.system())
        )

    io_glob.logger.debug(io_glob.LOGGER_END)


# -----------------------------------------------------------------------------
# Test case: launcher() - u_p_d   - Complete processing of a modifying MS Access
#                                   file.
# -----------------------------------------------------------------------------
# pylint: disable=R0801
def test_launcher_u_p_d():
    """Test case: launcher()."""
    # -------------------------------------------------------------------------
    io_glob.logger.debug(io_glob.LOGGER_START)

    assert settings.check_value == "test"

    if platform.system() == "Windows":
        os.system("run_io_avstats_pytest.bat u_p_d up22FEB")
    elif platform.system() == "Linux":
        os.system("./run_io_avstats_pytest.sh u_p_d up22FEB")
    else:
        # ERROR.00.908 The operating system '{os}' is not supported
        io_utils.terminate_fatal(
            io_glob.ERROR_00_908.replace("{os}", platform.system())
        )

    io_glob.logger.debug(io_glob.LOGGER_END)


# -----------------------------------------------------------------------------
# Test case: launcher() - r_d_s   - Refresh the PostgreSQL database schema.
# -----------------------------------------------------------------------------
# pylint: disable=R0801
def _test_launcher_r_d_s():
    """Test case: launcher()."""
    # -------------------------------------------------------------------------
    io_glob.logger.debug(io_glob.LOGGER_START)

    assert settings.check_value == "test"

    if platform.system() == "Windows":
        os.system("run_io_avstats_pytest.bat r_d_s")
    elif platform.system() == "Linux":
        os.system("./run_io_avstats_pytest.sh r_d_s")
    else:
        # ERROR.00.908 The operating system '{os}' is not supported
        io_utils.terminate_fatal(
            io_glob.ERROR_00_908.replace("{os}", platform.system())
        )

    io_glob.logger.debug(io_glob.LOGGER_END)
