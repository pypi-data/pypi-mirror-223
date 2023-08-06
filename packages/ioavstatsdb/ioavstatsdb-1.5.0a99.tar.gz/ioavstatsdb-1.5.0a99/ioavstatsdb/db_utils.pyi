# Copyright (c) 2022-2023 IO-Aero. All rights reserved. Use of this
# source code is governed by the IO-Aero License, that can
# be found in the LICENSE.md file.

"""Module stub file."""
import pyodbc  # type: ignore
from psycopg2 import connection
from psycopg2 import cursor

from ioavstatsdb import io_config

def get_msaccess_cursor(filename: str) -> tuple[pyodbc.Connection, pyodbc.Cursor]: ...
def get_postgres_cursor() -> tuple[connection, cursor]: ...
def get_postgres_cursor_admin(
    dbname=io_config.settings.postgres_dbname_admin,
) -> tuple[connection, cursor,]: ...
def upd_io_processed_files(file_name: str, cur_pg: cursor) -> None: ...
