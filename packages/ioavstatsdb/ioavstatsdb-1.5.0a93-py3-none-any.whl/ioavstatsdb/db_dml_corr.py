# Copyright (c) 2022-2023 IO-Aero. All rights reserved. Use of this
# source code is governed by the IO-Aero License, that can
# be found in the LICENSE.md file.

"""Managing the database schema of the PostgreSQL database."""
import os
from collections import OrderedDict

import lat_lon_parser  # type: ignore
from haversine import Unit  # type: ignore
from haversine import haversine
from openpyxl import load_workbook
from psycopg2.extensions import connection
from psycopg2.extensions import cursor

from ioavstatsdb import db_utils
from ioavstatsdb import io_config
from ioavstatsdb import io_glob
from ioavstatsdb import io_utils
from ioavstatsdb.io_utils import prepare_latitude
from ioavstatsdb.io_utils import prepare_longitude

# pylint: disable=too-many-lines

COLUMN_NAME: str = ""
COUNT_ERROR = 0
COUNT_SELECT = 0
COUNT_UPDATE = 0

EV_ID: str = ""

ROW: list[OrderedDict]
ROW_COLUMN_TABLE_NAME_IDX = 0
ROW_COLUMN_COLUMN_NAME_IDX = 1
ROW_COLUMN_VALUE_IDX = 2
ROW_COLUMN_EV_ID_IDX = 3
ROW_COLUMN_AIRCRAFT_KEY_IDX = 4
ROW_COLUMN_CREW_NO_IDX = 5
ROW_COLUMN_OCCURRENCE_NO_IDX = 6
ROW_COLUMN_NOTE_1_IDX = 7
ROW_COLUMN_NOTE_2_IDX = 8
ROW_COLUMN_NOTE_3_IDX = 9

TABLE_NAME: str = ""

VALUE: str = ""


# ------------------------------------------------------------------
# Check the corrected value column.
# ------------------------------------------------------------------
def _check_corrected_value() -> bool:
    if COLUMN_NAME == "io_latitude":
        try:
            lat_lon_parser.parse(prepare_latitude(VALUE))

            return True
        except ValueError:
            _error_msg(io_glob.ERROR_00_920)

    if COLUMN_NAME == "io_longitude":
        try:
            lat_lon_parser.parse(prepare_longitude(VALUE))

            return True
        except ValueError:
            _error_msg(io_glob.ERROR_00_921)

    return False


# ------------------------------------------------------------------
# Check the existence of an event with the given identification.
# ------------------------------------------------------------------
def _check_events_ev_id(cur_pg: cursor) -> bool:
    cur_pg.execute(
        f"""
    SELECT *
      FROM events
     WHERE ev_id = '{EV_ID}'
        """,
    )

    row_pg = cur_pg.fetchone()

    if row_pg:  # type: ignore
        return True

    # ERROR.00.931 The ev_id is missing in database table events
    _error_msg(io_glob.ERROR_00_931)

    return False


# ------------------------------------------------------------------
# Cleansing a database column.
# ------------------------------------------------------------------
def _cleansing_database_column(
    conn_pg: connection, cur_pg: cursor, table: str, column: str
):
    # INFO.00.066 Cleansing table '{table}' column '{column}'
    io_utils.progress_msg(
        io_glob.INFO_00_066.replace("{table}", table).replace("{column}", column)
    )

    # ------------------------------------------------------------------
    # Trimming data.
    # ------------------------------------------------------------------
    cur_pg.execute(
        f"""
        UPDATE {table}
           SET {column} = Trim({column})
        WHERE Length({column}) <> Length(Trim({column}));
        """,
    )

    if cur_pg.rowcount > 0:
        conn_pg.commit()
        io_utils.progress_msg(f"Number cols trimmed  : {str(cur_pg.rowcount):>8}")

    # ------------------------------------------------------------------
    # Converting data to NULL.
    # ------------------------------------------------------------------
    cur_pg.execute(
        f"""
        UPDATE {table}
           SET {column} = NULL
        WHERE Length({column}) = 0;
        """,
    )

    if cur_pg.rowcount > 0:
        conn_pg.commit()
        io_utils.progress_msg(f"Number cols nullified: {str(cur_pg.rowcount):>8}")


# ------------------------------------------------------------------
# Delete the missing aircraft.
# ------------------------------------------------------------------
def _delete_missing_aircraft(
    table_name: str,
    conn_pg: connection,
    cur_pg: cursor,
    cur_pg_2: cursor,
) -> None:
    io_glob.logger.debug(io_glob.LOGGER_START)

    count_delete = 0
    count_select = 0

    io_utils.progress_msg("")
    io_utils.progress_msg(
        f"Database table       : {table_name.lower():30}" + "<" + "-" * 35
    )

    cur_pg_2.execute(
        f"""
        SELECT n.ev_id, 
               n.aircraft_key
          FROM {table_name} n LEFT OUTER JOIN io_pk_ntsb ipn
                                ON ipn.table_name = %s
                               AND ipn.aircraft_key = n.aircraft_key
                               AND ipn.ev_id = n.ev_id
         WHERE  ipn.ev_id IS null
         """,
        (table_name,),
    )

    rows_tbd = cur_pg_2.fetchall()

    # pylint: disable=R0801
    for row_tbd in rows_tbd:
        count_select += 1

        if count_select % io_config.settings.database_commit_size == 0:
            conn_pg.commit()
            io_utils.progress_msg(
                f"Number of rows so far read : {str(count_select):>8}"
            )

        (ev_id, aircraft_key) = row_tbd

        # pylint: disable=line-too-long
        cur_pg.execute(
            f"""
        DELETE FROM {table_name}
         WHERE aircraft_key = %s
           AND ev_id = %s
        """,
            (
                aircraft_key,
                ev_id,
            ),
        )

        if cur_pg.rowcount > 0:
            count_delete += cur_pg.rowcount
            io_utils.progress_msg(f"Deleted  ev_id={ev_id} aircraft_key={aircraft_key}")

    conn_pg.commit()

    io_utils.progress_msg(f"Number rows selected : {str(count_select):>8}")

    if count_delete > 0:
        io_utils.progress_msg(f"Number rows deleted  : {str(count_delete):>8}")

    io_glob.logger.debug(io_glob.LOGGER_END)


# ------------------------------------------------------------------
# Create an error message.
# ------------------------------------------------------------------
def _error_msg(msg: str) -> None:
    global COUNT_ERROR  # pylint: disable=global-statement

    print(f"Row #{COUNT_SELECT + 1:4}: {ROW}")
    print(f"has error: {msg}")

    COUNT_ERROR += 1


# ------------------------------------------------------------------
# Process correction request for database table events.
# ------------------------------------------------------------------
# pylint: disable=too-many-return-statements
def _process_events(
    cur_pg: cursor,
) -> None:
    global COLUMN_NAME  # pylint: disable=global-statement
    global VALUE  # pylint: disable=global-statement
    global EV_ID  # pylint: disable=global-statement

    # pylint: disable=line-too-long
    COLUMN_NAME = ROW[ROW_COLUMN_COLUMN_NAME_IDX].value.lower() if ROW[ROW_COLUMN_COLUMN_NAME_IDX].value else None  # type: ignore
    if not COLUMN_NAME:
        # ERROR.00.930 Excel column '{column_name}' must not be empty
        _error_msg(io_glob.ERROR_00_930.replace("{column_name}", "column_name"))
        return

    if COLUMN_NAME not in [
        "io_city",
        "io_country",
        "io_latitude",
        "io_longitude",
        "io_site_zipcode",
        "io_state",
    ]:
        # ERROR.00.928 Database table column not yet supported
        _error_msg(io_glob.ERROR_00_928)
        return

    VALUE = ROW[ROW_COLUMN_VALUE_IDX].value  # type: ignore
    if not VALUE:
        # ERROR.00.930 Excel column '{column_name}' must not be empty
        _error_msg(io_glob.ERROR_00_930.replace("{column_name}", "value"))
        return

    if VALUE.lower() == "null":
        VALUE = "null"
    else:
        if COLUMN_NAME in [
            "io_latitude",
            "io_longitude",
        ]:
            if not _check_corrected_value():
                return

    EV_ID = ROW[ROW_COLUMN_EV_ID_IDX].value  # type: ignore
    if not EV_ID:
        # ERROR.00.930 Excel column '{column_name}' must not be empty
        _error_msg(io_glob.ERROR_00_930.replace("{column_name}", "ev_id"))
        return

    if not _check_events_ev_id(cur_pg):
        return

    if ROW[ROW_COLUMN_AIRCRAFT_KEY_IDX].value:  # type: ignore
        # ERROR.00.929 Excel column '{column_name}' must be empty
        _error_msg(io_glob.ERROR_00_929.replace("{column_name}", "aircraft_key"))
        return

    if ROW[ROW_COLUMN_CREW_NO_IDX].value:  # type: ignore
        # ERROR.00.929 Excel column '{column_name}' must be empty
        _error_msg(io_glob.ERROR_00_929.replace("{column_name}", "crew_no"))
        return

    if ROW[ROW_COLUMN_OCCURRENCE_NO_IDX].value:  # type: ignore
        # ERROR.00.929 Excel column '{column_name}' must be empty
        _error_msg(io_glob.ERROR_00_929.replace("{column_name}", "occurrence_no"))
        return

    _upd_table_events_row(cur_pg)


# ------------------------------------------------------------------
# Execute a query that returns the list of airport data.
# ------------------------------------------------------------------
def _sql_query_io_airports(conn_pg: connection) -> list[tuple[int, float, float]]:
    with conn_pg.cursor() as cur:  # type: ignore
        cur.execute(
            """
        SELECT global_id,
               dec_latitude,
               dec_longitude 
          FROM io_airports;
        """
        )

        data = []

        for row in cur:
            data.append(
                (
                    row[0],
                    row[1],
                    row[2],
                )
            )

        return sorted(data)


# ------------------------------------------------------------------
# Update the database table row.
# ------------------------------------------------------------------
def _upd_table_events_row(cur_pg: cursor) -> None:
    global COUNT_UPDATE  # pylint: disable=global-statement

    if VALUE == "null":
        cur_pg.execute(
            f"""
        UPDATE events SET
               {COLUMN_NAME} = NULL
         WHERE
               ev_id = %s
           AND {COLUMN_NAME} IS NOT NULL;
        """,
            (EV_ID,),
        )
    else:
        cur_pg.execute(
            f"""
        UPDATE events SET
               {COLUMN_NAME} = %s
         WHERE
               ev_id = %s
           AND ({COLUMN_NAME} IS NULL
            OR  {COLUMN_NAME} <> %s);
        """,
            (
                VALUE,
                EV_ID,
                VALUE,
            ),
        )

    COUNT_UPDATE += cur_pg.rowcount


# ------------------------------------------------------------------
# Update latitude and longitude.
# ------------------------------------------------------------------
# flake8: noqa: E501
def _upd_table_events_row_io_lat_lng(  # pylint: disable=too-many-arguments
    ev_id: str,
    io_dec_lat_lng_actions: str,
    io_dec_latitude: float | None,
    io_dec_longitude: float | None,
    io_latlong_acq: str,
    cur_pg: cursor,
) -> int:
    # pylint: disable=line-too-long
    cur_pg.execute(
        """
    UPDATE events SET
           io_dec_lat_lng_actions = %s,
           io_dec_latitude = %s,
           io_dec_longitude = %s,
           io_latlong_acq = %s
     WHERE
           ev_id = %s;
    """,
        (
            io_dec_lat_lng_actions,
            io_dec_latitude,
            io_dec_longitude,
            io_latlong_acq,
            ev_id,
        ),
    )
    return cur_pg.rowcount


# ------------------------------------------------------------------
# Update next airport data.
# ------------------------------------------------------------------
# flake8: noqa: E501
def _upd_table_events_row_next_airport(  # pylint: disable=too-many-arguments
    ev_id: str,
    nearest_airport_distance: float,
    nearest_airport_id: int,
    cur_pg: cursor,
) -> int:
    # pylint: disable=line-too-long
    cur_pg.execute(
        """
    UPDATE events SET
           io_nearest_airport_distance = %s,
           io_nearest_airport_global_id = %s
     WHERE
           ev_id = %s;
    """,
        (
            nearest_airport_distance,
            nearest_airport_id,
            ev_id,
        ),
    )
    return cur_pg.rowcount


# ------------------------------------------------------------------
# Cleansing PostgreSQL data.
# ------------------------------------------------------------------
# pylint: disable=too-many-branches
# pylint: disable=too-many-locals
# pylint: disable=too-many-statements
def cleansing_postgres_data() -> None:
    """Cleansing PostgreSQL data."""
    io_glob.logger.debug(io_glob.LOGGER_START)

    conn_pg, cur_pg = db_utils.get_postgres_cursor()

    conn_pg.set_session(autocommit=False)

    # ------------------------------------------------------------------
    # Database table events.
    # ------------------------------------------------------------------

    _cleansing_database_column(conn_pg, cur_pg, "aircraft", "acft_category")
    io_utils.progress_msg("-" * 80)
    _cleansing_database_column(conn_pg, cur_pg, "aircraft", "dest_country")
    io_utils.progress_msg("-" * 80)
    _cleansing_database_column(conn_pg, cur_pg, "aircraft", "dprt_country")
    io_utils.progress_msg("-" * 80)
    _cleansing_database_column(conn_pg, cur_pg, "aircraft", "far_part")
    io_utils.progress_msg("-" * 80)
    _cleansing_database_column(conn_pg, cur_pg, "aircraft", "oper_country")
    io_utils.progress_msg("-" * 80)
    _cleansing_database_column(conn_pg, cur_pg, "aircraft", "owner_country")
    io_utils.progress_msg("-" * 80)
    _cleansing_database_column(conn_pg, cur_pg, "aircraft", "regis_no")
    io_utils.progress_msg("-" * 80)
    _cleansing_database_column(conn_pg, cur_pg, "events", "ev_city")
    io_utils.progress_msg("-" * 80)
    _cleansing_database_column(conn_pg, cur_pg, "events", "ev_site_zipcode")
    io_utils.progress_msg("-" * 80)
    _cleansing_database_column(conn_pg, cur_pg, "events", "latitude")
    io_utils.progress_msg("-" * 80)
    _cleansing_database_column(conn_pg, cur_pg, "events", "longitude")
    io_utils.progress_msg("-" * 80)
    _cleansing_database_column(conn_pg, cur_pg, "events_sequence", "occurrence_code")

    # ------------------------------------------------------------------
    # Finalize processing.
    # ------------------------------------------------------------------
    cur_pg.close()
    conn_pg.close()

    io_glob.logger.debug(io_glob.LOGGER_END)


# ------------------------------------------------------------------
# Correct decimal latitude and longitude.
# ------------------------------------------------------------------
# pylint: disable=too-many-branches
# pylint: disable=too-many-locals
# pylint: disable=too-many-statements
def correct_dec_lat_lng() -> None:
    """Correct decimal latitude and longitude."""
    io_glob.logger.debug(io_glob.LOGGER_START)

    count_select = 0
    count_update = 0

    conn_pg, cur_pg = db_utils.get_postgres_cursor()

    conn_pg.set_session(autocommit=False)

    # ------------------------------------------------------------------
    # Delete existing data.
    # ------------------------------------------------------------------
    cur_pg.execute(
        """
    UPDATE events
    SET io_dec_lat_lng_actions = NULL,
        io_dec_latitude = NULL,
        io_dec_longitude = NULL,
        io_latlong_acq = NULL
    WHERE io_dec_lat_lng_actions IS NOT NULL
       OR io_dec_latitude IS NOT NULL
       OR io_dec_longitude IS NOT NULL
       OR io_latlong_acq IS NOT NULL;
    """,
    )

    if cur_pg.rowcount > 0:
        conn_pg.commit()

        io_utils.progress_msg(io_glob.INFO_00_063.replace("{data_source}", "events"))
        io_utils.progress_msg(f"Number cols deleted  : {str(cur_pg.rowcount):>8}")
        io_utils.progress_msg("-" * 80)

    # ------------------------------------------------------------------
    # Process events with missing decimal latitude or longitude.
    # ------------------------------------------------------------------
    conn_pg_2, cur_pg_2 = db_utils.get_postgres_cursor()

    conn_pg_2.set_session(autocommit=False)

    # pylint: disable=line-too-long
    cur_pg_2.execute(
        """
    SELECT *
      FROM io_lat_lng_issues
     ORDER BY ev_id;
        """,
    )

    for row_pg in cur_pg_2.fetchall():
        count_select += 1

        if count_select % io_config.settings.database_commit_size == 0:
            conn_pg.commit()
            io_utils.progress_msg(
                f"Number of rows so far read : {str(count_select):>8}"
            )

        # ------------------------------------------------------------------
        # Correct based on latitude and longitude.
        # ------------------------------------------------------------------
        io_dec_lat_lng_actions = ""
        io_dec_latitude = None
        io_dec_longitude = None

        ev_id = row_pg["ev_id"]  # type: ignore
        latitude = row_pg["latitude"]  # type: ignore
        longitude = row_pg["longitude"]  # type: ignore

        state = row_pg["state"]  # type: ignore
        if state not in io_glob.US_STATE_IDS:
            io_dec_lat_lng_actions = io_glob.ERROR_00_922

        if latitude and longitude:
            if latitude[-1] in ["E", "W"]:
                io_longitude, io_latitude = latitude, longitude
                latitude, longitude = io_latitude, io_longitude
                io_dec_lat_lng_actions = (
                    io_dec_lat_lng_actions + " & " + io_glob.INFO_00_038
                    if io_dec_lat_lng_actions
                    else io_glob.INFO_00_038
                )
                io_latlong_acq = "LOLA"
            else:
                io_dec_lat_lng_actions = (
                    io_dec_lat_lng_actions + " & " + io_glob.INFO_00_037
                    if io_dec_lat_lng_actions
                    else io_glob.INFO_00_037
                )
                io_latlong_acq = "LALO"
            try:
                io_dec_latitude = lat_lon_parser.parse(prepare_latitude(latitude))
            except ValueError:
                io_dec_lat_lng_actions = (
                    io_dec_lat_lng_actions + " & " + io_glob.ERROR_00_920
                    if io_dec_lat_lng_actions
                    else io_glob.ERROR_00_920
                )
                io_latlong_acq = "ERRA"
            try:
                io_dec_longitude = lat_lon_parser.parse(prepare_longitude(longitude))
            except ValueError:
                io_dec_lat_lng_actions = (
                    io_dec_lat_lng_actions + " & " + io_glob.ERROR_00_921
                    if io_dec_lat_lng_actions
                    else io_glob.ERROR_00_921
                )
                io_latlong_acq = "ERRO"
            if io_dec_latitude or io_dec_longitude:
                count_update += _upd_table_events_row_io_lat_lng(
                    ev_id,
                    io_dec_lat_lng_actions,
                    io_dec_latitude,
                    io_dec_longitude,
                    io_latlong_acq,
                    cur_pg,
                )
                continue

        # ------------------------------------------------------------------
        # Correct based on US zipcode.
        # ------------------------------------------------------------------
        if row_pg["country"] != "USA":  # type: ignore
            continue

        site_zipcode = row_pg["site_zipcode"]  # type: ignore
        dec_latitude = row_pg["zipcode_dec_latitude"]  # type: ignore
        dec_longitude = row_pg["zipcode_dec_longitude"]  # type: ignore

        if site_zipcode:
            if dec_latitude or dec_longitude:
                count_update += _upd_table_events_row_io_lat_lng(
                    ev_id,
                    io_dec_lat_lng_actions + " & " + io_glob.INFO_00_033
                    if io_dec_lat_lng_actions
                    else io_glob.INFO_00_033,
                    dec_latitude,
                    dec_longitude,
                    "ZIP",
                    cur_pg,
                )
                continue
            io_dec_lat_lng_actions = (
                io_dec_lat_lng_actions + " & " + io_glob.ERROR_00_915
                if io_dec_lat_lng_actions
                else io_glob.ERROR_00_915
            )

        # ------------------------------------------------------------------
        # Correct based on US city.
        # ------------------------------------------------------------------
        city = row_pg["city"]  # type: ignore
        dec_latitude = row_pg["city_dec_latitude"]  # type: ignore
        dec_longitude = row_pg["city_dec_longitude"]  # type: ignore

        if city:
            if dec_latitude or dec_longitude:
                count_update += _upd_table_events_row_io_lat_lng(
                    ev_id,
                    io_dec_lat_lng_actions + " & " + io_glob.INFO_00_034
                    if io_dec_lat_lng_actions
                    else io_glob.INFO_00_034,
                    dec_latitude,
                    dec_longitude,
                    "CITY",
                    cur_pg,
                )
                continue
            io_dec_lat_lng_actions = (
                io_dec_lat_lng_actions + " & " + io_glob.ERROR_00_916
                if io_dec_lat_lng_actions
                else io_glob.ERROR_00_916
            )

        # ------------------------------------------------------------------
        # Correct based on US state.
        # ------------------------------------------------------------------
        dec_latitude = row_pg["state_dec_latitude"]  # type: ignore
        dec_longitude = row_pg["state_dec_longitude"]  # type: ignore

        if state:
            if dec_latitude or dec_longitude:
                count_update += _upd_table_events_row_io_lat_lng(
                    ev_id,
                    io_dec_lat_lng_actions + " & " + io_glob.INFO_00_035
                    if io_dec_lat_lng_actions
                    else io_glob.INFO_00_035,
                    dec_latitude,
                    dec_longitude,
                    "STAT",
                    cur_pg,
                )
                continue
            io_dec_lat_lng_actions = (
                io_dec_lat_lng_actions + " & " + io_glob.ERROR_00_917
                if io_dec_lat_lng_actions
                else io_glob.ERROR_00_917
            )

        # ------------------------------------------------------------------
        # Correct based on US country.
        # ------------------------------------------------------------------
        dec_latitude = row_pg["country_dec_latitude"]  # type: ignore
        dec_longitude = row_pg["country_dec_longitude"]  # type: ignore

        count_update += _upd_table_events_row_io_lat_lng(
            ev_id,
            io_dec_lat_lng_actions + " & " + io_glob.INFO_00_036
            if io_dec_lat_lng_actions
            else io_glob.INFO_00_036,
            dec_latitude,
            dec_longitude,
            "COUN",
            cur_pg,
        )

    # ------------------------------------------------------------------
    # Finalize processing.
    # ------------------------------------------------------------------
    conn_pg.commit()

    cur_pg.close()
    conn_pg.close()

    cur_pg_2.close()
    conn_pg_2.close()

    io_utils.progress_msg(f"Number rows selected : {str(count_select):>8}")

    if count_update > 0:
        io_utils.progress_msg(f"Number rows updated  : {str(count_update):>8}")

    io_glob.logger.debug(io_glob.LOGGER_END)


# ------------------------------------------------------------------
# Find the nearest airports.
# ------------------------------------------------------------------
def find_nearest_airports() -> None:
    """Find the nearest airports."""
    io_glob.logger.debug(io_glob.LOGGER_START)

    count_select = 0
    count_update = 0

    conn_pg, cur_pg = db_utils.get_postgres_cursor()

    conn_pg.set_session(autocommit=False)

    # ------------------------------------------------------------------
    # Delete existing data.
    # ------------------------------------------------------------------
    cur_pg.execute(
        """
    UPDATE events
    SET io_nearest_airport_distance = NULL,
        io_nearest_airport_global_id = NULL
    WHERE io_nearest_airport_distance IS NOT NULL
       OR io_nearest_airport_global_id IS NOT NULL;
    """,
    )

    if cur_pg.rowcount > 0:
        conn_pg.commit()

        io_utils.progress_msg(io_glob.INFO_00_063.replace("{data_source}", "events"))
        io_utils.progress_msg(f"Number cols deleted  : {str(cur_pg.rowcount):>8}")
        io_utils.progress_msg("-" * 80)

    # ------------------------------------------------------------------
    # Process events with missing nearest airport data.
    # ------------------------------------------------------------------
    conn_pg_2, cur_pg_2 = db_utils.get_postgres_cursor()

    conn_pg_2.set_session(autocommit=False)

    airports = _sql_query_io_airports(conn_pg_2)

    # pylint: disable=line-too-long
    cur_pg_2.execute(
        """
    SELECT ev_id,
           COALESCE(io_dec_latitude,  e.dec_latitude)  dec_latitude,
           COALESCE(io_dec_longitude, e.dec_longitude) dec_longitude
      FROM events e LEFT OUTER JOIN io_states i 
                    ON (e.ev_state   = i.state
                    AND e.ev_country = i.country)
     WHERE COALESCE(io_dec_latitude,  e.dec_latitude)  IS NOT NULL
       AND COALESCE(io_dec_longitude, e.dec_longitude) IS NOT NULL
       AND i.state IS NOT NULL
       AND ev_country = 'USA'
     ORDER BY COALESCE(io_dec_latitude,  e.dec_latitude),
              COALESCE(io_dec_longitude, e.dec_longitude)
        """,
    )

    prev_ev_dec_latitude = -999999.9
    prev_ev_dec_longitude = -999999.9
    prev_nearest_airport_distance = 999999
    prev_nearest_airport_id = 0

    for row_pg in cur_pg_2.fetchall():
        count_select += 1

        if count_select % io_config.settings.database_commit_size == 0:
            conn_pg.commit()
            io_utils.progress_msg(
                f"Number of rows so far read : {str(count_select):>8}"
            )

        ev_id = row_pg["ev_id"]  # type: ignore
        ev_dec_latitude = row_pg["dec_latitude"]  # type: ignore
        ev_dec_longitude = row_pg["dec_longitude"]  # type: ignore

        if (
            ev_dec_latitude == prev_ev_dec_latitude
            and ev_dec_longitude == prev_ev_dec_longitude
        ):
            count_update += _upd_table_events_row_next_airport(
                ev_id,
                prev_nearest_airport_distance,
                prev_nearest_airport_id,
                cur_pg,
            )
            continue

        nearest_airport_distance = 999999
        nearest_airport_id = 0

        for ap_id, ap_dec_latitude, ap_dec_longitude in airports:
            try:
                distance = haversine(
                    (
                        ev_dec_latitude,
                        ev_dec_longitude,
                    ),
                    (
                        ap_dec_latitude,
                        ap_dec_longitude,
                    ),
                    unit=Unit.MILES,
                )
            except ValueError as err:
                # ERROR.00.942 Issue with the Harvesine algorithm: '{error}'
                io_utils.progress_msg(
                    io_glob.ERROR_00_942.replace("{ev_id}", ev_id).replace(
                        "{error}", str(err)
                    )
                )
                break
            if distance < nearest_airport_distance:
                nearest_airport_distance = distance
                nearest_airport_id = ap_id

        if nearest_airport_distance < 999999:
            count_update += _upd_table_events_row_next_airport(
                ev_id,
                nearest_airport_distance,
                nearest_airport_id,
                cur_pg,
            )

            prev_ev_dec_latitude = ev_dec_latitude
            prev_ev_dec_longitude = ev_dec_longitude
            prev_nearest_airport_distance = nearest_airport_distance
            prev_nearest_airport_id = nearest_airport_id

    # ------------------------------------------------------------------
    # Finalize processing.
    # ------------------------------------------------------------------
    conn_pg.commit()

    cur_pg.close()
    conn_pg.close()

    cur_pg_2.close()
    conn_pg_2.close()

    io_utils.progress_msg(f"Number rows selected : {str(count_select):>8}")

    if count_update > 0:
        io_utils.progress_msg(f"Number rows updated  : {str(count_update):>8}")

    io_glob.logger.debug(io_glob.LOGGER_END)


# ------------------------------------------------------------------
# Load data from a correction file into the PostgreSQL database.
# ------------------------------------------------------------------
def load_correction_data(filename: str) -> None:
    """Load data from a correction file into the PostgreSQL database.

    Args:
        filename (str):
            The MS Excel file.
    """
    global COUNT_SELECT  # pylint: disable=global-statement
    global ROW  # pylint: disable=global-statement
    global TABLE_NAME  # pylint: disable=global-statement

    io_glob.logger.debug(io_glob.LOGGER_START)

    corr_file = os.path.join(io_config.settings.correction_work_dir, filename)

    if not os.path.isfile(corr_file):
        # ERROR.00.926 The correction file '{filename}' is missing
        io_utils.terminate_fatal(io_glob.ERROR_00_926.replace("{filename}", corr_file))

    conn_pg, cur_pg = db_utils.get_postgres_cursor()

    conn_pg.set_session(autocommit=False)

    workbook = load_workbook(
        filename=corr_file,
        read_only=True,
        data_only=True,
    )

    # pylint: disable=R0801
    for ROW in workbook.active:
        # pylint: disable=line-too-long
        TABLE_NAME = ROW[ROW_COLUMN_TABLE_NAME_IDX].value.lower() if ROW[ROW_COLUMN_TABLE_NAME_IDX].value else None  # type: ignore
        if TABLE_NAME == "table_name":
            continue

        COUNT_SELECT += 1

        if COUNT_SELECT % io_config.settings.database_commit_size == 0:
            conn_pg.commit()
            io_utils.progress_msg(
                f"Number of rows so far read : {str(COUNT_SELECT):>8}"
            )

        # ERROR.00.930 Excel column '{column_name}' must not be empty
        if not TABLE_NAME:
            _error_msg(io_glob.ERROR_00_930.replace("{column_name}", "table_name"))
            continue

        if TABLE_NAME == io_glob.TABLE_NAME_EVENTS:
            _process_events(cur_pg)
        else:
            _error_msg(io_glob.ERROR_00_927)

    workbook.close()

    conn_pg.commit()

    io_utils.progress_msg(f"Number rows selected : {str(COUNT_SELECT):>8}")

    if COUNT_UPDATE > 0:
        io_utils.progress_msg(f"Number rows updated  : {str(COUNT_UPDATE):>8}")

    if COUNT_ERROR > 0:
        io_utils.progress_msg(f"Number rows erroneous: {str(COUNT_ERROR):>8}")

    cur_pg.close()
    conn_pg.close()

    io_glob.logger.debug(io_glob.LOGGER_END)


# ------------------------------------------------------------------
# Verify selected NTSB data.
# ------------------------------------------------------------------
# pylint: disable=too-many-branches
# pylint: disable=too-many-locals
# pylint: disable=too-many-statements
def verify_ntsb_data() -> None:
    """Verify selected NTSB data."""
    io_glob.logger.debug(io_glob.LOGGER_START)

    # ------------------------------------------------------------------
    # Resetting the error markers.
    # ------------------------------------------------------------------
    conn_pg, cur_pg = db_utils.get_postgres_cursor()

    conn_pg.set_session(autocommit=False)

    cur_pg.execute(
        """
    UPDATE
        events
    SET
        io_dec_latitude_deviating = NULL,
        io_dec_longitude_deviating = NULL,
        io_invalid_latitude = FALSE,
        io_invalid_longitude = FALSE,
        io_invalid_us_city = FALSE,
        io_invalid_us_city_zipcode = FALSE,
        io_invalid_us_state = FALSE,
        io_invalid_us_zipcode = FALSE
    WHERE
           io_dec_latitude_deviating IS NOT NULL
        OR io_dec_longitude_deviating IS NOT NULL
        OR io_invalid_latitude IS NOT FALSE
        OR io_invalid_longitude IS NOT FALSE
        OR io_invalid_us_city IS NOT FALSE
        OR io_invalid_us_city_zipcode IS NOT FALSE
        OR io_invalid_us_state IS NOT FALSE
        OR io_invalid_us_zipcode IS NOT FALSE
    """
    )

    if cur_pg.rowcount > 0:
        conn_pg.commit()

        io_utils.progress_msg(io_glob.INFO_00_063.replace("{data_source}", "events"))
        io_utils.progress_msg(f"Number cols deleted  : {str(cur_pg.rowcount):>8}")
        io_utils.progress_msg("-" * 80)

    count_errors = 0
    count_select = 0
    count_update = 0

    conn_pg_2, cur_pg_2 = db_utils.get_postgres_cursor()

    conn_pg_2.set_session(autocommit=False)

    # ------------------------------------------------------------------
    # Verify latitude & longitude.
    # ------------------------------------------------------------------
    # INFO.00.064 Verification of table '{table}' column(s) '{column}'"
    io_utils.progress_msg(
        io_glob.INFO_00_064.replace("{table}", "events").replace(
            "{column}", "latitude & longitude"
        )
    )
    io_utils.progress_msg("-" * 80)

    cur_pg_2.execute(
        """
        SELECT e.ev_id ev_id,
               e.latitude latitude,
               e.longitude longitude,
               e.dec_latitude dec_latitude,
               e.dec_longitude dec_longitude,
               e.io_dec_latitude io_dec_latitude,
               e.io_dec_longitude io_dec_longitude
          FROM events e
         WHERE e.latitude IS NOT NULL
            OR e.longitude IS NOT NULL
         ORDER BY e.ev_id
    """
    )

    # pylint: disable=R0801
    # pylint: disable=too-many-nested-blocks
    for row_pg in cur_pg_2.fetchall():
        count_select += 1

        if count_select % io_config.settings.database_commit_size == 0:
            conn_pg.commit()
            io_utils.progress_msg(
                f"Number of rows so far read : {str(count_select):>8}"
            )

        io_dec_latitude_deviating = None
        io_dec_longitude_deviating = None
        io_invalid_latitude = False
        io_invalid_longitude = False

        # ------------------------------------------------------------------
        # Invalid latitude.
        # ------------------------------------------------------------------
        latitude = row_pg["latitude"]  # type: ignore

        if latitude:
            try:
                dec_latitude_comp = lat_lon_parser.parse(prepare_latitude(latitude))

                dec_latitude = row_pg["dec_latitude"]  # type: ignore
                if dec_latitude:
                    deviation = abs(dec_latitude - dec_latitude_comp)
                    if deviation > io_config.settings.max_deviation_latitude:
                        io_dec_latitude_deviating = deviation
                        count_errors += 1
            except ValueError:
                io_invalid_latitude = True
                count_errors += 1

        # ------------------------------------------------------------------
        # Invalid longitude.
        # ------------------------------------------------------------------
        longitude = row_pg["longitude"]  # type: ignore

        if longitude:
            try:
                dec_longitude_comp = lat_lon_parser.parse(prepare_longitude(longitude))

                dec_longitude = row_pg["dec_longitude"]  # type: ignore
                if dec_longitude:
                    deviation = abs(dec_longitude - dec_longitude_comp)
                    if deviation > io_config.settings.max_deviation_longitude:
                        io_dec_longitude_deviating = deviation
                        count_errors += 1
            except ValueError:
                io_invalid_longitude = True
                count_errors += 1

        # ------------------------------------------------------------------
        # Update error flags.
        # ------------------------------------------------------------------
        if not (
            io_dec_latitude_deviating is None
            and io_dec_longitude_deviating is None
            and io_invalid_latitude is False
            and io_invalid_longitude is False
        ):
            ev_id = row_pg["ev_id"]  # type: ignore
            cur_pg.execute(
                """
            UPDATE events SET
                io_dec_latitude_deviating = %s,
                io_dec_longitude_deviating = %s,
                io_invalid_latitude = %s,
                io_invalid_longitude = %s
             WHERE
                 ev_id = %s;
            """,
                (
                    io_dec_latitude_deviating,
                    io_dec_longitude_deviating,
                    io_invalid_latitude,
                    io_invalid_longitude,
                    ev_id,
                ),
            )
            count_update += cur_pg.rowcount

    if count_errors > 0:
        io_utils.progress_msg(f"Number rows errors   : {str(count_update):>8}")
    io_utils.progress_msg("-" * 80)

    # ------------------------------------------------------------------
    # Verify city.
    # ------------------------------------------------------------------
    # INFO.00.064 Verification of table '{table}' column(s) '{column}'"
    io_utils.progress_msg(
        io_glob.INFO_00_064.replace("{table}", "events").replace("{column}", "ev_city")
    )

    cur_pg.execute(
        """
        UPDATE events
           SET io_invalid_us_city = TRUE
         WHERE ev_id IN (   SELECT e.ev_id ev_id
                              FROM events e
                              LEFT OUTER JOIN io_lat_lng ll
                                ON (   ll.city  = UPPER(e.ev_city)
                                 AND   ll.state = e.ev_state
                                 and   ll.type  = 'CITY')
                             WHERE ll.city IS NULL
                               and e.ev_city IS NOT NULL
                               AND e.ev_country = 'USA' )
        """,
    )

    count_errors += cur_pg.rowcount
    count_update += cur_pg.rowcount

    if cur_pg.rowcount > 0:
        io_utils.progress_msg(f"Number rows errors   : {str(cur_pg.rowcount):>8}")
    io_utils.progress_msg("-" * 80)

    # ------------------------------------------------------------------
    # Verify city & zipcode.
    # ------------------------------------------------------------------
    # INFO.00.064 Verification of table '{table}' column(s) '{column}'"
    io_utils.progress_msg(
        io_glob.INFO_00_064.replace("{table}", "events").replace(
            "{column}", "ev_city & ev_site_zipcode"
        )
    )

    cur_pg.execute(
        """
        UPDATE events
           SET io_invalid_us_city_zipcode = TRUE
         WHERE ev_id IN (   SELECT e.ev_id ev_id
                              FROM events e
                              LEFT OUTER JOIN io_lat_lng ll
                                ON (   ll.zipcode = e.ev_site_zipcode
                                 AND   ll.city    = UPPER(e.ev_city)
                                 AND   ll.state   = e.ev_state
                                 and   ll.type    = 'ZIPCODE')
                             WHERE ll.city IS NULL
                               AND e.ev_site_zipcode IS NOT NULL
                               and e.ev_city IS NOT NULL
                               AND e.ev_country = 'USA' )
        """,
    )

    count_errors += cur_pg.rowcount
    count_update += cur_pg.rowcount

    if cur_pg.rowcount > 0:
        io_utils.progress_msg(f"Number rows errors   : {str(cur_pg.rowcount):>8}")
    io_utils.progress_msg("-" * 80)

    # ------------------------------------------------------------------
    # Verify state.
    # ------------------------------------------------------------------
    # INFO.00.064 Verification of table '{table}' column(s) '{column}'"
    io_utils.progress_msg(
        io_glob.INFO_00_064.replace("{table}", "events").replace("{column}", "ev_state")
    )

    cur_pg.execute(
        """
        UPDATE events
           SET io_invalid_us_state = TRUE
         WHERE ev_id IN (   SELECT e.ev_id ev_id
                              FROM events e
                              LEFT OUTER JOIN io_states s
                                ON (s.state = e.ev_state)
                             WHERE s.state IS null
                               AND e.ev_country = 'USA' )
        """,
    )

    count_errors += cur_pg.rowcount
    count_update += cur_pg.rowcount

    if cur_pg.rowcount > 0:
        io_utils.progress_msg(f"Number rows errors   : {str(cur_pg.rowcount):>8}")
    io_utils.progress_msg("-" * 80)

    # ------------------------------------------------------------------
    # Verify zipcode.
    # ------------------------------------------------------------------
    # INFO.00.064 Verification of table '{table}' column(s) '{column}'"
    io_utils.progress_msg(
        io_glob.INFO_00_064.replace("{table}", "events").replace(
            "{column}", "ev_site_zipcode"
        )
    )

    cur_pg.execute(
        """
        UPDATE events
           SET io_invalid_us_zipcode = TRUE
         WHERE ev_id IN (   SELECT e.ev_id ev_id
                              FROM events e
                              LEFT OUTER JOIN io_lat_lng ll
                                ON (   ll.zipcode = e.ev_site_zipcode
                                 and   ll.type    = 'ZIPCODE')
                             WHERE ll.zipcode IS null
                               and e.ev_site_zipcode is not null
                               AND e.ev_country = 'USA' )
          """,
    )

    count_errors += cur_pg.rowcount
    count_update += cur_pg.rowcount

    if cur_pg.rowcount > 0:
        io_utils.progress_msg(f"Number rows errors   : {str(cur_pg.rowcount):>8}")
    io_utils.progress_msg("-" * 80)

    cur_pg.close()
    conn_pg.close()

    cur_pg_2.close()
    conn_pg_2.close()

    io_utils.progress_msg(f"Number rows selected : {str(count_select):>8}")

    if count_update > 0:
        io_utils.progress_msg(f"Number rows updated  : {str(count_update):>8}")

    if count_errors > 0:
        io_utils.progress_msg(f"Number rows errors   : {str(count_update):>8}")

    io_glob.logger.debug(io_glob.LOGGER_END)
