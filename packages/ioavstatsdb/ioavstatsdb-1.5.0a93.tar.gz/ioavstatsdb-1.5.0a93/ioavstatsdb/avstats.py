# Copyright (c) 2022-2023 IO-Aero. All rights reserved. Use of this
# source code is governed by the IO-Aero License, that can
# be found in the LICENSE.md file.

"""IO-AVSTATS-DB interface."""
from __future__ import annotations

import argparse
import os
import zipfile

from openpyxl.reader.excel import load_workbook
from openpyxl.utils.exceptions import InvalidFileException  # type: ignore

from ioavstatsdb import code_generator
from ioavstatsdb import db_ddl_base
from ioavstatsdb import db_dml_base
from ioavstatsdb import db_dml_corr
from ioavstatsdb import io_config
from ioavstatsdb import io_glob
from ioavstatsdb import io_utils

# -----------------------------------------------------------------------------
# Global variables.
# -----------------------------------------------------------------------------

ARG_MSACCESS = ""
ARG_MSEXCEL = ""
ARG_TASK = ""


# -----------------------------------------------------------------------------
# Check the command line argument: -m / --msaccess.
# -----------------------------------------------------------------------------
def check_arg_msaccess(args: argparse.Namespace) -> None:
    """Check the command line argument: -m / --msaccess.

    Args:
        args (argparse.Namespace): Command line arguments.
    """
    global ARG_MSACCESS  # pylint: disable=global-statement

    if ARG_TASK in [
        io_glob.ARG_TASK_D_N_A,
        io_glob.ARG_TASK_L_N_A,
    ]:
        if not args.msaccess:
            # ERROR.00.901 The task '{task}' requires valid
            # argument '-m' or '--msaccess'
            terminate_fatal(io_glob.ERROR_00_901.replace("{task}", ARG_TASK))
    else:
        if args.msaccess:
            # ERROR.00.902 The task '{task}' does not require an
            # argument '-m' or '--msaccess'
            terminate_fatal(io_glob.ERROR_00_902.replace("{task}", ARG_TASK))
        else:
            return

    ARG_MSACCESS = args.msaccess.lower()

    if ARG_MSACCESS == io_glob.ARG_MSACCESS_AVALL:
        return

    if ARG_MSACCESS == io_glob.ARG_MSACCESS_PRE2008.lower():
        ARG_MSACCESS = io_glob.ARG_MSACCESS_PRE2008
        return

    if "." in ARG_MSACCESS:
        # ERROR.00.904 '{msaccess}': the MS Access database file name must not
        # contain a file extension
        terminate_fatal(io_glob.ERROR_00_904.replace("{msaccess}", args.msaccess))

    if not (
        ARG_MSACCESS[0:2] == "up"
        and "00" < ARG_MSACCESS[2:4] <= "31"
        and ARG_MSACCESS[4:]
        in [
            "jan",
            "feb",
            "mar",
            "apr",
            "may",
            "jun",
            "jul",
            "aug",
            "sep",
            "oct",
            "nov",
            "dec",
        ]
    ):
        # ERROR.00.903 '{msaccess}' is not a valid NTSB compliant
        # MS Access database name
        terminate_fatal(io_glob.ERROR_00_903.replace("{msaccess}", args.msaccess))

    ARG_MSACCESS = ARG_MSACCESS[0:4] + ARG_MSACCESS[4:].upper()


# -----------------------------------------------------------------------------
# Check the command line argument: -e / --msexcel.
# -----------------------------------------------------------------------------
def check_arg_msexcel(args: argparse.Namespace) -> None:
    """Check the command line argument: -e / --msexcel.

    Args:
        args (argparse.Namespace): Command line arguments.
    """
    global ARG_MSEXCEL  # pylint: disable=global-statement

    if ARG_TASK in [io_glob.ARG_TASK_L_C_D]:
        if not args.msexcel:
            # ERROR.00.923 The task '{task}' requires valid
            # argument '-e' or '--msexcel'
            terminate_fatal(io_glob.ERROR_00_923.replace("{task}", ARG_TASK))
    else:
        if args.msexcel:
            # ERROR.00.924 The task '{task}' does not require an
            # argument '-e' or '--msexcel'
            terminate_fatal(io_glob.ERROR_00_924.replace("{task}", ARG_TASK))
        else:
            return

    directory_name = ""
    if ARG_TASK == io_glob.ARG_TASK_L_C_D:
        directory_name = io_config.settings.correction_work_dir

    ARG_MSEXCEL = args.msexcel

    if ARG_TASK in [io_glob.ARG_TASK_L_C_D, io_glob.ARG_TASK_L_C_D]:
        file_name = os.path.join(directory_name, ARG_MSEXCEL)
    else:
        file_name = os.path.join(directory_name, ARG_MSEXCEL + ".xlsx")

    try:
        load_workbook(
            filename=file_name,
            read_only=True,
            data_only=True,
        )
    except FileNotFoundError:
        # ERROR.00.932 File '{filename}' is not existing
        terminate_fatal(io_glob.ERROR_00_932.replace("{filename}", file_name))
    except (InvalidFileException, zipfile.BadZipFile):
        # ERROR.00.925 '{msexcel}' is not a valid Microsoft Excel file
        terminate_fatal(io_glob.ERROR_00_925.replace("{msexcel}", file_name))


# -----------------------------------------------------------------------------
# Check the command line argument: -t / --task.
# -----------------------------------------------------------------------------
def check_arg_task(args: argparse.Namespace) -> None:
    """Check the command line argument: -t / --task.

    Args:
        args (argparse.Namespace): Command line arguments.
    """
    global ARG_TASK  # pylint: disable=global-statement

    ARG_TASK = args.task.lower()

    if not (
        ARG_TASK
        in [
            io_glob.ARG_TASK_A_O_C,
            io_glob.ARG_TASK_C_D_S,
            io_glob.ARG_TASK_C_L_L,
            io_glob.ARG_TASK_C_P_D,
            io_glob.ARG_TASK_D_N_A,
            io_glob.ARG_TASK_F_N_A,
            io_glob.ARG_TASK_GENERATE,
            io_glob.ARG_TASK_L_A_P,
            io_glob.ARG_TASK_L_C_D,
            io_glob.ARG_TASK_L_C_S,
            io_glob.ARG_TASK_L_N_A,
            io_glob.ARG_TASK_L_S_D,
            io_glob.ARG_TASK_L_S_E,
            io_glob.ARG_TASK_L_Z_D,
            io_glob.ARG_TASK_R_D_S,
            io_glob.ARG_TASK_U_D_S,
            io_glob.ARG_TASK_VERSION,
            io_glob.ARG_TASK_V_N_D,
        ]
    ):
        terminate_fatal(
            "The specified task is neither '"
            + io_glob.ARG_TASK_A_O_C
            + "' nor '"
            + io_glob.ARG_TASK_C_D_S
            + "' nor '"
            + io_glob.ARG_TASK_C_L_L
            + "' nor '"
            + io_glob.ARG_TASK_C_P_D
            + "' nor '"
            + io_glob.ARG_TASK_D_N_A
            + "' nor '"
            + io_glob.ARG_TASK_F_N_A
            + "' nor '"
            + io_glob.ARG_TASK_GENERATE
            + "' nor '"
            + io_glob.ARG_TASK_L_A_P
            + "' nor '"
            + io_glob.ARG_TASK_L_C_D
            + "' nor '"
            + io_glob.ARG_TASK_L_C_S
            + "' nor '"
            + io_glob.ARG_TASK_L_N_A
            + "' nor '"
            + io_glob.ARG_TASK_L_S_D
            + "' nor '"
            + io_glob.ARG_TASK_L_S_E
            + "' nor '"
            + io_glob.ARG_TASK_L_Z_D
            + "' nor '"
            + io_glob.ARG_TASK_R_D_S
            + "' nor '"
            + io_glob.ARG_TASK_U_D_S
            + "' nor '"
            + io_glob.ARG_TASK_VERSION
            + "' nor '"
            + io_glob.ARG_TASK_V_N_D
            + f"': {args.task}",
        )


# ------------------------------------------------------------------
# c_p_d: Cleansing PostgreSQL data.
# ------------------------------------------------------------------
def cleansing_postgres_data() -> None:
    """c_p_d: Cleansing PostgreSQL data."""
    io_glob.logger.debug(io_glob.LOGGER_START)

    # INFO.00.065 Cleansing PostgreSQL data
    io_utils.progress_msg(io_glob.INFO_00_065)
    io_utils.progress_msg("-" * 80)

    db_dml_corr.cleansing_postgres_data()

    io_glob.logger.debug(io_glob.LOGGER_END)


# ------------------------------------------------------------------
# c_l_l: Correct US decimal latitudes and longitudes.
# ------------------------------------------------------------------
def correct_dec_lat_lng() -> None:
    """c_l_l: Correct US decimal latitudes and longitudes."""
    io_glob.logger.debug(io_glob.LOGGER_START)

    # INFO.00.040 Correct decimal US latitudes and longitudes
    io_utils.progress_msg(io_glob.INFO_00_040)
    io_utils.progress_msg("-" * 80)

    db_dml_corr.correct_dec_lat_lng()

    io_glob.logger.debug(io_glob.LOGGER_END)


# ------------------------------------------------------------------
# c_d_s: Create the PostgreSQL database schema.
# ------------------------------------------------------------------
def create_db_schema() -> None:
    """c_d_s: Create the PostgreSQL database schema."""
    io_glob.logger.debug(io_glob.LOGGER_START)

    # INFO.00.044 Creating the database schema
    io_utils.progress_msg(io_glob.INFO_00_044)
    io_utils.progress_msg("-" * 80)

    db_ddl_base.create_db_schema()

    io_glob.logger.debug(io_glob.LOGGER_END)


# ------------------------------------------------------------------
# d_n_a: Download a NTSB MS Access database file.
# ------------------------------------------------------------------
def download_ntsb_msaccess_file(msaccess: str) -> None:
    """d_n_a: Download a NTSB MS Access database file.

    Args:
        msaccess (str):
            The NTSB MS Access database file without file extension.
    """
    io_glob.logger.debug(io_glob.LOGGER_START)

    # INFO.00.047 Download NTSB MS Access database file '{msaccess}'
    io_utils.progress_msg(io_glob.INFO_00_047.replace("{msaccess}", msaccess))
    io_utils.progress_msg("-" * 80)

    db_dml_base.download_ntsb_msaccess_file(msaccess)

    io_glob.logger.debug(io_glob.LOGGER_END)


# ------------------------------------------------------------------
# f_n_a: Find the nearest airports.
# ------------------------------------------------------------------
def find_nearest_airports() -> None:
    """f_n_a: Find the nearest airports."""
    io_glob.logger.debug(io_glob.LOGGER_START)

    # INFO.00.086 Find the nearest airports
    io_utils.progress_msg(io_glob.INFO_00_086)
    io_utils.progress_msg("-" * 80)

    db_dml_corr.find_nearest_airports()

    io_glob.logger.debug(io_glob.LOGGER_END)


# -----------------------------------------------------------------------------
# Generate SQL statements: INSERT & UPDATE.
# -----------------------------------------------------------------------------
def generate_sql() -> None:
    """Generate SQL statements: INSERT & UPDATE."""
    io_glob.logger.debug(io_glob.LOGGER_START)

    code_generator.generate_sql()

    io_glob.logger.debug(io_glob.LOGGER_END)


# -----------------------------------------------------------------------------
# Initialising the logging functionality.
# -----------------------------------------------------------------------------
def initialise_logger() -> None:
    """Initialise the root logging functionality."""
    io_utils.initialise_logger()


# -----------------------------------------------------------------------------
# Load the command line arguments into the memory.
# -----------------------------------------------------------------------------
def get_args() -> None:
    """Load the command line arguments into the memory."""
    io_glob.logger.debug(io_glob.LOGGER_START)

    parser = argparse.ArgumentParser(
        description="Perform a IO-AVSTATS-DB task",
        prog="launcher",
        prefix_chars="--",
        usage="%(prog)s options",
    )

    # -------------------------------------------------------------------------
    # Definition of the command line arguments.
    # ------------------------------------------------------------------------
    parser.add_argument(
        "-e",
        "--msexcel",
        help="the MS Excel file: '",
        metavar="msexcel",
        required=False,
        type=str,
    )

    parser.add_argument(
        "-m",
        "--msaccess",
        help="the microsoft access database file: '"
        + io_glob.ARG_MSACCESS_AVALL
        + "' (Data from January 1, 2008 to today) or '"
        + io_glob.ARG_MSACCESS_PRE2008
        + "' (Data from January 1, 1982 to December 31, 2007) or '"
        + io_glob.ARG_MSACCESS_UPDDMON
        + "' (New additions and updates until DD day in the month MON)",
        metavar="msaccess",
        required=False,
        type=str,
    )

    parser.add_argument(
        "-t",
        "--task",
        help="the task to execute: '"
        + io_glob.ARG_TASK_A_O_C
        + "' (Load aviation occurrence categories into PostgreSQL) or '"
        + io_glob.ARG_TASK_C_D_S
        + "' (Create the PostgreSQL database schema) or '"
        + io_glob.ARG_TASK_C_L_L
        + "' (Correct decimal US latitudes and longitudes) or '"
        + io_glob.ARG_TASK_C_P_D
        + "' (Cleansing PostgreSQL data) or '"
        + io_glob.ARG_TASK_D_N_A
        + "' (Download a NTSB MS Access database file) or '"
        + io_glob.ARG_TASK_F_N_A
        + "' (Find the nearest airports) or '"
        + io_glob.ARG_TASK_GENERATE
        + "' (Generate SQL statements) or '"
        + io_glob.ARG_TASK_L_A_P
        + "' (Load airport data into PostgreSQL) or '"
        + io_glob.ARG_TASK_L_C_D
        + "' (Load data from a correction file into PostgreSQL) or '"
        + io_glob.ARG_TASK_L_C_S
        + "' (Load country and state data into PostgreSQL) or '"
        + io_glob.ARG_TASK_L_N_A
        + "' (Load NTSB MS Access database data into PostgreSQL) or '"
        + io_glob.ARG_TASK_L_S_D
        + "' (Load simplemaps data into PostgreSQL) or '"
        + io_glob.ARG_TASK_L_S_E
        + "' (Load sequence of events data into PostgreSQL) or '"
        + io_glob.ARG_TASK_L_Z_D
        + "' (Load ZIP Code Database data into PostgreSQL) or '"
        + io_glob.ARG_TASK_R_D_S
        + "' (Update the PostgreSQL database schema) or '"
        + io_glob.ARG_TASK_U_D_S
        + "' (Refresh the PostgreSQL database schema) or '"
        + io_glob.ARG_TASK_VERSION
        + "' (Show the current version of IO-AVSTATS)"
        + io_glob.ARG_TASK_V_N_D
        + "' (Verify selected **NTSB** data) or '",
        metavar="task",
        required=True,
        type=str,
    )

    # -------------------------------------------------------------------------
    # Load and check the command line arguments.
    # -------------------------------------------------------------------------
    parsed_args = parser.parse_args()

    check_arg_task(parsed_args)

    check_arg_msaccess(parsed_args)

    check_arg_msexcel(parsed_args)

    # --------------------------------------------------------------------------
    # Display the command line arguments.
    # --------------------------------------------------------------------------
    if parsed_args.msexcel:
        # INFO.00.041 Arguments {task}='{value_task}' {msexcel}='{value_msexcel}'
        progress_msg(
            io_glob.INFO_00_041.replace("{task}", io_glob.ARG_TASK)
            .replace("{value_task}", parsed_args.task)
            .replace("{msexcel}", io_glob.ARG_MSEXCEL)
            .replace("{value_msexcel}", parsed_args.msexcel),
        )
    elif parsed_args.msaccess:
        # INFO.00.008 Arguments {task}='{value_task}' {msaccess}='{value_msaccess}'
        progress_msg(
            io_glob.INFO_00_008.replace("{task}", io_glob.ARG_TASK)
            .replace("{value_task}", parsed_args.task)
            .replace("{msaccess}", io_glob.ARG_MSACCESS)
            .replace("{value_msaccess}", parsed_args.msaccess),
        )
    else:
        # INFO.00.005 Arguments {task}='{value_task}'
        progress_msg(
            io_glob.INFO_00_005.replace("{task}", io_glob.ARG_TASK).replace(
                "{value_task}", parsed_args.task
            ),
        )

    io_glob.logger.debug(io_glob.LOGGER_END)


# ------------------------------------------------------------------
# a_o_c: Load aviation occurrence categories into PostgreSQL.
# ------------------------------------------------------------------
def load_aviation_occurrence_categories() -> None:
    """a_o_c: Load aviation occurrence categories into PostgreSQL."""
    io_glob.logger.debug(io_glob.LOGGER_START)

    # INFO.00.073 Load aviation occurrence categories
    io_utils.progress_msg(io_glob.INFO_00_073)
    io_utils.progress_msg("-" * 80)

    db_dml_base.load_aviation_occurrence_categories()

    io_glob.logger.debug(io_glob.LOGGER_END)


# ------------------------------------------------------------------
# l_a_p: Load airport data into PostgreSQL.
# ------------------------------------------------------------------
def load_airport_data() -> None:
    """l_a_p: Load airport data into PostgreSQL."""
    io_glob.logger.debug(io_glob.LOGGER_START)

    # INFO.00.085 Load airports
    io_utils.progress_msg(io_glob.INFO_00_085)
    io_utils.progress_msg("-" * 80)

    db_dml_base.load_airport_data()

    io_glob.logger.debug(io_glob.LOGGER_END)


# ------------------------------------------------------------------
# l_c_d: Load data from a correction file into PostgreSQL.
# ------------------------------------------------------------------
def load_correction_data(filename: str) -> None:
    """l_c_d: Load data from a correction file into PostgreSQL.

    Args:
        filename (str):
            The filename of the correction file.
    """
    io_glob.logger.debug(io_glob.LOGGER_START)

    # INFO.00.042 Load corrections from file '{filename}'
    io_utils.progress_msg(io_glob.INFO_00_042.replace("{filename}", filename))
    io_utils.progress_msg("-" * 80)

    db_dml_corr.load_correction_data(filename)

    io_glob.logger.debug(io_glob.LOGGER_END)


# ------------------------------------------------------------------
# l_c_s: Load country and state data into PostgreSQL.
# ------------------------------------------------------------------
def load_country_state_data() -> None:
    """l_c_s: Load country and state data into PostgreSQL."""
    io_glob.logger.debug(io_glob.LOGGER_START)

    # INFO.00.057 Load country and state data
    io_utils.progress_msg(io_glob.INFO_00_057)
    io_utils.progress_msg("-" * 80)

    db_dml_base.load_country_state_data()

    io_glob.logger.debug(io_glob.LOGGER_END)


# ------------------------------------------------------------------
# l_n_a: Load NTSB MS Access database data into PostgreSQL.
# ------------------------------------------------------------------
def load_ntsb_msaccess_data(msaccess: str) -> None:
    """l_n_a: Load NTSB MS Access database data into PostgreSQL.

    Args:
        msaccess (str):
            The NTSB MS Access database file without file extension.
    """
    io_glob.logger.debug(io_glob.LOGGER_START)

    # INFO.00.049 Load NTSB MS Access database data from file '{msaccess}'
    io_utils.progress_msg(io_glob.INFO_00_049.replace("{msaccess}", msaccess))
    io_utils.progress_msg("-" * 80)

    db_dml_base.load_ntsb_msaccess_data(msaccess)

    io_glob.logger.debug(io_glob.LOGGER_END)


# ------------------------------------------------------------------
# l_s_e: Load sequence of events data into PostgreSQL.
# ------------------------------------------------------------------
def load_sequence_of_events() -> None:
    """l_s_e: Load sequence of events data into PostgreSQL."""
    io_glob.logger.debug(io_glob.LOGGER_START)

    # INFO.00.075 Load sequence of events data
    io_utils.progress_msg(io_glob.INFO_00_075)
    io_utils.progress_msg("-" * 80)

    db_dml_base.load_sequence_of_events()

    io_glob.logger.debug(io_glob.LOGGER_END)


# ------------------------------------------------------------------
# l_s_d: Load simplemaps data into PostgreSQL.
# ------------------------------------------------------------------
def load_simplemaps_data() -> None:
    """l_s_d: Load simplemaps data into PostgreSQL."""
    io_glob.logger.debug(io_glob.LOGGER_START)

    # INFO.00.050 Load simplemaps data
    io_utils.progress_msg(io_glob.INFO_00_050)
    io_utils.progress_msg("-" * 80)

    db_dml_base.load_simplemaps_data()

    io_glob.logger.debug(io_glob.LOGGER_END)


# ------------------------------------------------------------------
# l_z_d: Load ZIP Code Database data into PostgreSQL.
# ------------------------------------------------------------------
def load_zip_code_db_data() -> None:
    """l_z_d: Load ZIP Code Database data into PostgreSQL."""
    io_glob.logger.debug(io_glob.LOGGER_START)

    # INFO.00.056 Load ZIP Code Database data
    io_utils.progress_msg(io_glob.INFO_00_056)
    io_utils.progress_msg("-" * 80)

    db_dml_base.load_zip_codes_org_data()

    io_glob.logger.debug(io_glob.LOGGER_END)


# ------------------------------------------------------------------
# Create a progress message.
# ------------------------------------------------------------------
def progress_msg(msg: str) -> None:
    """Create a progress message.

    Args:
        msg (str): Progress message
    """
    if io_config.settings.is_verbose:
        io_utils.progress_msg_core(msg)


# ------------------------------------------------------------------
# Create a progress message.
# ------------------------------------------------------------------
def progress_msg_time_elapsed(duration: int, event: str) -> None:
    """Create a time elapsed message.

    Args:
        duration (int): Time elapsed in ns.
        event (str): Event description.
    """
    io_utils.progress_msg_time_elapsed(duration, event)


# ------------------------------------------------------------------
# r_d_s: Refresh the PostgreSQL database schema.
# ------------------------------------------------------------------
def refresh_db_schema() -> None:
    """r_d_s: Refresh the PostgreSQL database schema."""
    io_glob.logger.debug(io_glob.LOGGER_START)

    # INFO.00.071 Refreshing the database schema
    io_utils.progress_msg(io_glob.INFO_00_071)
    io_utils.progress_msg("-" * 80)

    db_ddl_base.refresh_db_schema()

    io_glob.logger.debug(io_glob.LOGGER_END)


# ------------------------------------------------------------------
# Terminate the application immediately.
# ------------------------------------------------------------------
def terminate_fatal(error_msg: str) -> None:
    """Terminate the application immediately.

    Args:
        error_msg (str): Error message
    """

    io_utils.terminate_fatal(error_msg)


# ------------------------------------------------------------------
# u_d_s: Update the PostgreSQL database schema.
# ------------------------------------------------------------------
def update_db_schema() -> None:
    """u_d_s: Update the PostgreSQL database schema."""
    io_glob.logger.debug(io_glob.LOGGER_START)

    # INFO.00.045 Updating the database schema
    io_utils.progress_msg(io_glob.INFO_00_045)
    io_utils.progress_msg("-" * 80)

    db_ddl_base.update_db_schema()

    io_glob.logger.debug(io_glob.LOGGER_END)


# ------------------------------------------------------------------
# v_n_d: Verify selected NTSB data.
# ------------------------------------------------------------------
def verify_ntsb_data() -> None:
    """v_n_d: Verify selected NTSB data."""
    io_glob.logger.debug(io_glob.LOGGER_START)

    # INFO.00.043 Verify selected NTSB data
    io_utils.progress_msg(io_glob.INFO_00_043)
    io_utils.progress_msg("-" * 80)

    db_dml_corr.verify_ntsb_data()

    io_glob.logger.debug(io_glob.LOGGER_END)


# ------------------------------------------------------------------
# Returns the version number of the IO-AVSTATS-DB application.
# ------------------------------------------------------------------
def version() -> str:
    """Returns the version number of the IO-AVSTATS-DB application.

    Returns:
        str:
            The version number of the IO-AVSTATS-DB application
    """
    io_glob.logger.debug(io_glob.LOGGER_START)
    io_glob.logger.debug(io_glob.LOGGER_END)

    return io_glob.IO_AVSTATS_DB_VERSION
