# Copyright (c) 2022-2023 IO-Aero. All rights reserved. Use of this
# source code is governed by the IO-Aero License, that can
# be found in the LICENSE.md file.

"""Managing the database schema of the PostgreSQL database."""
import os
from datetime import datetime
from pathlib import Path

import psycopg2
import psycopg2.extras
import pyodbc  # type: ignore
from psycopg2.extensions import connection
from psycopg2.extensions import cursor

from ioavstatsdb import io_config
from ioavstatsdb import io_glob
from ioavstatsdb import io_utils


# ------------------------------------------------------------------
# Create a PostgreSQL connection.
# ------------------------------------------------------------------
# pylint: disable=inconsistent-return-statements
# pylint: disable=too-many-arguments
def _get_postgres_connection(  # type: ignore
    autocommit: bool, dbname: str, host: str, password: str, port: int, user: str
) -> connection:
    """Create a PostgreSQL connection.

    Args:
        autocommit (bool): Sets the autocommit behavior of the database connection.
        dbname (str): Database name.
        host (str): Host name.
        password (str): Password.
        port (int): Port number.
        user (str): User name.

    Returns:
        connection: PostgreSQL database connection.
    """
    try:
        conn = psycopg2.connect(
            database=dbname,
            user=user,
            password=password,
            host=host,
            port=port,
        )

        conn.autocommit = autocommit

        return conn

    except psycopg2.OperationalError as exc:
        # INFO.00.091 User connect request host={host} port={port} dbname={dbname}
        # user={user} password={password}
        io_utils.progress_msg(
            io_glob.INFO_00_091.replace("{host}", host)
            .replace("{port}", str(port))
            .replace("{dbname}", dbname)
            .replace("{user}", user)
            .replace("{password}", password)
        )
        io_utils.terminate_fatal(str(exc))


# ------------------------------------------------------------------
# Create a PostgreSQL connection and cursor.
# ------------------------------------------------------------------
# pylint: disable=inconsistent-return-statements
# pylint: disable=too-many-arguments
def _get_postgres_cursor(
    autocommit: bool, dbname: str, host: str, password: str, port: int, user: str
) -> tuple[connection, cursor]:
    """Create a PostgreSQL connection and cursor.

    Args:
        autocommit (bool): Sets the autocommit behavior of the database connection.
        dbname (str): _description_
        host (str): _description_
        password (str): _description_
        port (int): _description_
        user (str): _description_

    Returns:
        tuple[connection, cursor]: PostgreSQL database connection and cursor.
    """
    conn_pg = _get_postgres_connection(
        autocommit=autocommit,
        dbname=dbname,
        host=host,
        password=password,
        port=port,
        user=user,
    )

    return conn_pg, conn_pg.cursor(cursor_factory=psycopg2.extras.DictCursor)


# ------------------------------------------------------------------
# Create an ODBC database connection and cursor.
# ------------------------------------------------------------------
def get_msaccess_cursor(filename: str) -> tuple[pyodbc.Connection, pyodbc.Cursor]:
    """Create an MS Access cursor.

    Args:
        filename (str): MS Access filename.

    Returns:
        tuple[pyodbc.Connection,pyodbc.Cursor]: ODBC database connection and cursor.
    """
    filename_mdb = os.getcwd() + os.path.sep + filename

    if not Path(filename_mdb).is_file():
        # ERROR.00.932 File '{filename}' is not existing
        io_utils.terminate_fatal(
            io_glob.ERROR_00_932.replace("{filename}", filename_mdb)
        )

    # Driver={Microsoft Access Driver (*.mdb, *.accdb)};DBQ={filename}}
    driver = io_config.settings.odbc_connection_string.replace(
        "{filename}", filename_mdb
    )

    # INFO.00.054 ODBC driver='{driver}'
    io_utils.progress_msg(io_glob.INFO_00_054.replace("{driver}", driver))

    conn_ma = pyodbc.connect(driver)  # pylint: disable=c-extension-no-member

    return conn_ma, conn_ma.cursor()


# ------------------------------------------------------------------
# Create a simple user PostgreSQL connection and cursor.
# ------------------------------------------------------------------
def get_postgres_cursor() -> tuple[connection, cursor]:
    """Create a simple user PostgreSQL connection and cursor.

    Returns:
        tuple[connection,cursor]: PostgreSQL database connection and cursor.
    """
    # INFO.00.081 User connect request host={host} port={port} dbname={dbname}
    # user={user}
    io_utils.progress_msg(
        io_glob.INFO_00_081.replace("{host}", io_config.settings.postgres_host)
        .replace("{port}", str(io_config.settings.postgres_connection_port))
        .replace("{dbname}", io_config.settings.postgres_dbname)
        .replace("{user}", io_config.settings.postgres_user)
    )

    return _get_postgres_cursor(
        autocommit=True,
        dbname=io_config.settings.postgres_dbname,
        host=io_config.settings.postgres_host,
        password=io_config.settings.postgres_password,
        port=io_config.settings.postgres_connection_port,
        user=io_config.settings.postgres_user,
    )


# ------------------------------------------------------------------
# Create an administrator PostgreSQL connection and cursor.
# ------------------------------------------------------------------
def get_postgres_cursor_admin(
    dbname=io_config.settings.postgres_dbname_admin,
) -> tuple[connection, cursor,]:
    """Create an administrator PostgreSQL connection and cursor.

    Returns:
        tuple[connection,cursor]: PostgreSQL database connection and cursor.
    """
    # INFO.00.080 Admin connect request host={host} port={port} dbname={dbname}
    # user={usG206er}
    io_utils.progress_msg(
        io_glob.INFO_00_080.replace("{host}", io_config.settings.postgres_host)
        .replace("{port}", str(io_config.settings.postgres_connection_port))
        .replace("{dbname}", dbname)
        .replace("{user}", io_config.settings.postgres_user_admin)
    )

    return _get_postgres_cursor(
        autocommit=True,
        dbname=dbname,
        host=io_config.settings.postgres_host,
        password=io_config.settings.postgres_password_admin,
        port=io_config.settings.postgres_connection_port,
        user=io_config.settings.postgres_user_admin,
    )


# ------------------------------------------------------------------
# Update the database table io_processed_files.
# ------------------------------------------------------------------
def upd_io_processed_files(file_name: str, cur_pg: cursor) -> None:
    """Update the database table io_processed_files."""
    io_glob.logger.debug(io_glob.LOGGER_START)

    cur_pg.execute(
        """
    INSERT INTO io_processed_files AS ipf (
           file_name,
           first_processed,
           counter
           ) VALUES (
           %s,%s,%s
           )
    ON CONFLICT ON CONSTRAINT io_processed_files_pkey
    DO UPDATE
       SET last_processed = %s,
           counter = ipf.counter + 1
     WHERE ipf.file_name = %s;
    """,
        (
            file_name,
            datetime.now(),
            1,
            datetime.now(),
            file_name,
        ),
    )

    io_glob.logger.debug(io_glob.LOGGER_END)
