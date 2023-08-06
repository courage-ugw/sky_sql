
# List of Queries for the project
QUERY_FLIGHT_BY_ID = """
SELECT 
    flights.*, 
    airlines.airline, 
    flights.ID AS FLIGHT_ID, 
    flights.DEPARTURE_DELAY AS DELAY
FROM 
    flights 
    JOIN airlines ON flights.airline = airlines.id
WHERE 
    flights.ID = :id;
"""

QUERY_FLIGHT_BY_AIRPORT = """
SELECT 
    flights.*, 
    airlines.airline, 
    flights.ID AS FLIGHT_ID, 
    flights.DEPARTURE_DELAY AS DELAY
FROM 
    flights 
    JOIN airlines ON flights.airline = airlines.id
WHERE 
    flights.ORIGIN_AIRPORT = :IATA;
"""

QUERY_FLIGHT_BY_DATE = """
SELECT 
    flights.*, 
    airlines.airline, 
    flights.ID AS FLIGHT_ID, 
    flights.DEPARTURE_DELAY AS DELAY
FROM 
    flights 
    JOIN airlines ON flights.airline = airlines.id
WHERE 
    flights.DAY = :day 
    AND flights.MONTH = :month 
    AND flights.YEAR = :year;
"""

QUERY_FLIGHT_BY_AIRLINE = """
SELECT 
    flights.ORIGIN_AIRPORT, 
    flights.DESTINATION_AIRPORT, 
    flights.DEPARTURE_DELAY AS DELAY, 
    airlines.airline, 
    airlines.ID AS ID
FROM 
    airlines 
    JOIN flights ON flights.airline = airlines.id
WHERE airlines.AIRLINE = :airline;
"""

QUERY_BY_DELAYED_AND_DEPARTED_FLIGHTS = """
SELECT
	airlines.AIRLINE,
	COUNT(CASE WHEN flights.DEPARTURE_DELAY > 0 THEN 1 END) AS num_of_delayed_flights,
	COUNT(flights.DEPARTURE_TIME) AS num_of_flights
FROM 
	flights
	JOIN airlines ON flights.AIRLINE = airlines.ID
GROUP BY airlines.airline
"""

QUERY_BY_ORIGIN_DESTINATION_DELAY = """
SELECT
    flights.ORIGIN_AIRPORT,
    flights.DESTINATION_AIRPORT,
    CAST(COUNT(CASE WHEN flights.DEPARTURE_DELAY > 0 THEN 1 END) * 100.0 / COUNT(*) AS INTEGER) AS percentage_delay
FROM
    flights
GROUP BY
    flights.ORIGIN_AIRPORT,
    flights.DESTINATION_AIRPORT;
"""

QUERY_AIRPORT_ORIGIN_DESTINATION_LAT_LONG = """
SELECT
    flights.ORIGIN_AIRPORT AS origin_airport,
    origin_airports.LATITUDE AS origin_latitude,
    origin_airports.LONGITUDE AS origin_longitude,
    flights.DESTINATION_AIRPORT AS destination_airport,
    dest_airports.LATITUDE AS destination_latitude,
    dest_airports.LONGITUDE AS destination_longitude,
	CAST(COUNT(CASE WHEN flights.DEPARTURE_DELAY > 0 THEN 1 END) * 100.0 / COUNT(*) AS INTEGER) AS percentage_delay
FROM
    flights
JOIN airports AS origin_airports ON flights.ORIGIN_AIRPORT = origin_airports.IATA_CODE
JOIN airports AS dest_airports ON flights.DESTINATION_AIRPORT = dest_airports.IATA_CODE

GROUP BY 
	origin_airport, destination_airport;
"""

QUERY_FLIGHT_BY_DELAY_AND_DEPARTURE_TIME = """
SELECT
	flights.DEPARTURE_TIME,
	CASE 
		WHEN flights.DEPARTURE_DELAY <= 0 THEN 0
		ELSE flights.DEPARTURE_DELAY
		END AS DELAY	
FROM
	flights
WHERE 
	DELAY IS NOT '' 
	AND DELAY IS NOT NULL
"""


# Other Queries.
"----------------------****************---------------*******************----------------************************"
"""
DATABASE can be found in data_db/flights.sqlite3
************************************************

SELECT
	flights.ID,
	flights.YEAR,
	flights.MONTH,
	flights.DAY,
	flights.ORIGIN_AIRPORT AS ORIGIN,
	flights.DESTINATION_AIRPORT AS DESTINATION,
	flights.AIRLINE_DELAY AS DELAY
FROM
	flights
WHERE
	flights.ID = 280;

*************************************************************
SELECT
	flights.ID,
	flights.YEAR,
	flights.MONTH,
	flights.DAY,
	flights.ORIGIN_AIRPORT AS ORIGIN,
	flights.DESTINATION_AIRPORT AS DESTINATION,
	airlines.AIRLINE As AIRLINE_NAME,
	flights.AIRLINE_DELAY AS DELAY
FROM
	flights
	JOIN airlines ON flights.AIRLINE = airlines.ID
WHERE
	flights.ID = 280;

***************************************************************

SELECT
	flights.ID,
	flights.ORIGIN_AIRPORT AS ORIGIN,
	flights.DESTINATION_AIRPORT AS DESTINATION,
	flights.AIRLINE_DELAY AS DELAY
FROM
	flights
WHERE
	flights.DAY = 1
	AND flights.MONTH = 3
	AND flights.YEAR = 2015
	AND DELAY IS NOT NULL
	AND DELAY != ''
ORDER BY
	DELAY DESC
LIMIT 5;

*******************************************************************

SELECT
	flights.ORIGIN_AIRPORT AS airport,
	COUNT(flights.DEPARTURE_TIME) AS total_departures
FROM
	flights
GROUP BY airport
LIMIT 10;

******************************************************************

SELECT
    airlines.AIRLINE As airline,
    ROUND(AVG(
        CASE
            WHEN flights.AIRLINE_DELAY = '' THEN 0
            ELSE flights.AIRLINE_DELAY
        END
    ), 4) AS average_delay
FROM
    flights
JOIN airlines ON flights.AIRLINE = airlines.ID
GROUP BY airlines.AIRLINE
ORDER BY average_delay DESC;

*******************************************************************

SELECT
    airlines.AIRLINE As airline,
    ROUND(AVG(flights.DEPARTURE_DELAY), 4) AS average_delay
FROM
    flights
JOIN airlines ON flights.AIRLINE = airlines.ID
GROUP BY airlines.AIRLINE
ORDER BY average_delay DESC;

*****************************************************************

SELECT
    airlines.AIRLINE As airline,
    ROUND(AVG(
        CASE
            WHEN flights.DEPARTURE_DELAY <= 0 THEN 0
            ELSE flights.AIRLINE_DELAY
        END
    ), 4) AS average_delay
FROM
    flights
JOIN airlines ON flights.AIRLINE = airlines.ID
GROUP BY airlines.AIRLINE
ORDER BY average_delay DESC;

********************************************************

SELECT
	airports.AIRPORT AS airport,
	COUNT(*) AS num_of_flights,
	ROUND(AVG(
		CASE
			WHEN flights.DEPARTURE_DELAY <= 0 THEN 0
			ELSE flights.DEPARTURE_DELAY
		END
		), 1) AS average_delay

FROM
	flights
	JOIN airports ON flights.ORIGIN_AIRPORT = airports.IATA_CODE
GROUP BY
	airport
HAVING
	num_of_flights > 5000
ORDER BY average_delay DESC
;

"""