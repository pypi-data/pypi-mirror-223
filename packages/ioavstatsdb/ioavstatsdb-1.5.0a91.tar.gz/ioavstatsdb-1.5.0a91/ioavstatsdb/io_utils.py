# Copyright (c) 2022-2023 IO-Aero. All rights reserved. Use of this
# source code is governed by the IO-Aero License, that can
# be found in the LICENSE.md file.

"""Miscellaneous helper functions."""
import datetime
import logging
import logging.config
import sys
import traceback

import yaml

from ioavstatsdb import io_config
from ioavstatsdb import io_glob

# ------------------------------------------------------------------
# Global constants.
# ------------------------------------------------------------------
_LOGGER_CFG_FILE = "logging_cfg.yaml"
_LOGGER_FATAL_HEAD = "FATAL ERROR: program abort =====> "
_LOGGER_FATAL_TAIL = " <===== FATAL ERROR"
_LOGGER_PROGRESS_UPDATE = "Progress update "


# -----------------------------------------------------------------------------
# Initialising the logging functionality.
# -----------------------------------------------------------------------------
def initialise_logger() -> None:
    """Initialise the root logging functionality."""
    with open(
        _LOGGER_CFG_FILE, "r", encoding=io_glob.FILE_ENCODING_DEFAULT
    ) as file_handle:
        log_config = yaml.safe_load(file_handle.read())

    logging.config.dictConfig(log_config)
    io_glob.logger.setLevel(logging.DEBUG)

    # The logger is configured and ready.
    progress_msg_core(io_glob.INFO_00_001)


# ------------------------------------------------------------------
# Create a progress message.
# ------------------------------------------------------------------
def progress_msg(msg: str) -> None:
    """Create a progress message.

    Args:
        msg (str): Progress message.
    """
    if io_config.settings.is_verbose:
        progress_msg_core(msg)


# -----------------------------------------------------------------------------
# Prepare a latitude structure.
# -----------------------------------------------------------------------------
# pylint: disable=too-many-return-statements
def prepare_latitude(latitude_string: str) -> str:
    """Prepare a latitude structure.

    Args:
        latitude_string (str): Latitude string.

    Returns:
        str: Latitude structure.
    """
    len_latitude_string = len(latitude_string)

    if len_latitude_string == 7:
        return (
            latitude_string[:2]
            + " "
            + latitude_string[2:4]
            + " "
            + latitude_string[4:6]
            + " "
            + latitude_string[6:]
        )

    if len_latitude_string == 6:
        return (
            latitude_string[:1]
            + " "
            + latitude_string[1:3]
            + " "
            + latitude_string[3:5]
            + " "
            + latitude_string[5:]
        )

    if len_latitude_string == 5:
        return (
            latitude_string[:2] + " " + latitude_string[2:4] + " " + latitude_string[4:]
        )

    if len_latitude_string == 4:
        return (
            latitude_string[:1] + " " + latitude_string[1:3] + " " + latitude_string[3:]
        )

    if len_latitude_string == 3:
        return latitude_string[:2] + " " + latitude_string[2:]

    if len_latitude_string == 2:
        return latitude_string[:1] + " " + latitude_string[1:]

    return latitude_string


# -----------------------------------------------------------------------------
# Prepare a longitude structure.
# -----------------------------------------------------------------------------
def prepare_longitude(longitude_string: str) -> str:
    """Prepare a longitude structure.

    Args:
        longitude_string (str): longitude string.

    Returns:
        str: longitude structure.
    """
    if len(longitude_string) == 8:
        return (
            longitude_string[:3]
            + " "
            + longitude_string[3:5]
            + " "
            + longitude_string[5:7]
            + " "
            + longitude_string[7:]
        )

    return prepare_latitude(longitude_string)


# ------------------------------------------------------------------
# Create a progress message.
# ------------------------------------------------------------------
def progress_msg_core(msg: str) -> None:
    """Create a progress message.

    Args:
        msg (str): Progress message.
    """
    final_msg = _LOGGER_PROGRESS_UPDATE + str(datetime.datetime.now()) + " : " + msg

    if msg not in ("", "-" * 80, "=" * 80):
        final_msg = final_msg + "."

    print(final_msg)


# ------------------------------------------------------------------
# Create a progress message.
# ------------------------------------------------------------------
def progress_msg_time_elapsed(duration: int, event: str) -> None:
    """Create a time elapsed message.

    Args:
        duration (int): Time elapsed in ns.
        event (str): Event description.
    """
    if io_config.settings.is_verbose:
        progress_msg_core(
            f"{f'{duration:,}':>20} ns - Total time {event}",
        )


# ------------------------------------------------------------------
# Terminate the application immediately.
# ------------------------------------------------------------------
def terminate_fatal(error_msg: str) -> None:
    """Terminate the application immediately.

    Args:
        error_msg (str): Error message.
    """
    print("")
    traceback.print_stack()
    print("")
    print(_LOGGER_FATAL_HEAD)
    print(_LOGGER_FATAL_HEAD, error_msg, _LOGGER_FATAL_TAIL, sep="")
    print(_LOGGER_FATAL_HEAD)

    sys.exit(1)
