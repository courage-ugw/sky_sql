from sqlalchemy import create_engine
from sql_queries import *


class FlightData:
    """
    The FlightData class is a Data Access Layer (DAL) object that provides an
    interface to the flight data_db in the SQLITE database. When the object is created,
    the class forms connection to the sqlite database file, which remains active
    until the object is destroyed.
    """

    def __init__(self, db_uri):
        """
        Initialize a new engine using the given database URI
        """
        self._engine = create_engine(db_uri)

    def _execute_query(self, query, params):
        """
        Execute an SQL query with the params provided in a dictionary,
        and returns a list of records (dictionary-like objects).
        If an exception was raised, print the error, and return an empty list.
        """
        if params is not None:
            try:
                with self._engine.connect() as connection:
                    result = connection.execute(query, params)
                    return result.fetchall()
            except Exception as e:
                print("Error:", e)
                return {}

        try:
            with self._engine.connect() as connection:
                result = connection.execute(query)
                return result.fetchall()
        except Exception as e:
            print("Error:", e)
            return {}

    def get_flight_by_id(self, flight_id):
        """
        Searches for flight details using flight ID.
        If the flight was found, returns a list with a single record.
        """
        params = {'id': flight_id}
        return self._execute_query(QUERY_FLIGHT_BY_ID, params)

    def get_delayed_flights_by_airport(self, airport_short_code):
        """
        Searches for flight details using airport IATA (3-letter) code.
        If the flight was found, returns a list with a single record.
        """
        params = {'IATA': airport_short_code}
        return self._execute_query(QUERY_FLIGHT_BY_AIRPORT, params)

    def get_delayed_flights_by_airline(self, airline_name):
        """
        Searches for flight details using airline name.
        If the flight was found, returns a list with a single record.
        """
        params = {'airline': airline_name}
        return self._execute_query(QUERY_FLIGHT_BY_AIRLINE, params)

    def get_flights_by_date(self, day, month, year):
        """
        Searches for flight details using date (day, month and year).
        If the flight was found, returns a list with a single record.
        """
        params = {
            'day': day,
            'month': month,
            'year': year
        }
        return self._execute_query(QUERY_FLIGHT_BY_DATE, params)

    def get_delayed_and_departed_flights_by_airline(self):
        """
        Searches for delayed and departed flight details.
        If the flight was found, returns a list with a single record.
        """
        return self._execute_query(QUERY_BY_DELAYED_AND_DEPARTED_FLIGHTS, params=None)

    def get_delay_and_departure_time(self):
        """
        Searches for flight delay and departure time.
        If the flight was found, returns a list with a single record.
        """
        return self._execute_query(QUERY_FLIGHT_BY_DELAY_AND_DEPARTURE_TIME, params=None)

    def get_origin_destination_airport_delay(self):
        """
        Searches for flight origin and destination airports including flight delays.
        If the flight was found, returns a list with a single record.
        """
        return self._execute_query(QUERY_BY_ORIGIN_DESTINATION_DELAY, params=None)

    def get_origin_destination_latitude_longitude(self):
        """
        Searches for flight origin and destination airports including their coordinates
        If the flight was found, returns a list with a single record.
        """
        return self._execute_query(QUERY_AIRPORT_ORIGIN_DESTINATION_LAT_LONG, params=None)

    def __del__(self):
        """
        Closes the connection to the databse when the object is about to be destroyed
        """
        self._engine.dispose()
