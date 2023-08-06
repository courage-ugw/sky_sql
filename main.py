from datetime import datetime
import sqlalchemy
import data
from data_plots import *

SQLITE_URI = 'sqlite:///flights.sqlite3'
IATA_LENGTH = 3


def delayed_flights_by_airline(data_manager):
    """
    Asks the user for a textual airline name (any string will work here).
    Then runs the query using the data_db object method "get_delayed_flights_by_airline".
    When results are back, calls "print_results" to show them to on the screen.
    """
    airline_input = input("Enter airline name: ")
    results = data_manager.get_delayed_flights_by_airline(airline_input)
    print_results(results)


def delayed_flights_by_airport(data_manager):
    """
    Asks the user for a textual IATA 3-letter airport code (loops until input is valid).
    Then runs the query using the data_db object method "get_delayed_flights_by_airport".
    When results are back, calls "print_results" to show them to on the screen.
    """
    valid = False
    while not valid:
        airport_input = input("Enter origin airport IATA code: ")
        # Valide input
        if airport_input.isalpha() and len(airport_input) == IATA_LENGTH:
            valid = True
    results = data_manager.get_delayed_flights_by_airport(airport_input)
    print_results(results)


def flight_by_id(data_manager):
    """
    Asks the user for a numeric flight ID,
    Then runs the query using the data_db object method "get_flight_by_id".
    When results are back, calls "print_results" to show them to on the screen.
    """
    valid = False
    while not valid:
        try:
            id_input = int(input("Enter flight ID: "))
        except Exception as e:
            print("Try again...")
        else:
            valid = True
    results = data_manager.get_flight_by_id(id_input)
    print_results(results)


def flights_by_date(data_manager):
    """
    Asks the user for date input (and loops until it's valid),
    Then runs the query using the data_db object method "get_flights_by_date".
    When results are back, calls "print_results" to show them to on the screen.
    """
    valid = False
    while not valid:
        try:
            date_input = input("Enter date in DD/MM/YYYY format: ")
            date = datetime.strptime(date_input, '%d/%m/%Y')
        except ValueError as e:
            print("Try again...", e)
        else:
            valid = True
    results = data_manager.get_flights_by_date(date.day, date.month, date.year)
    print_results(results)


def percentage_of_delayed_flights_per_airline(data_manager):
    """
    When selected by the user. This function gets the delayed flights by airline
    and calculates the percentage the of delay. If no exception errors, it parses
    the results to the visualize data result function to display the chart plot
    to the user. The visual_type is also specified.
    """
    # Get flight data
    flights_data = data_manager.get_delayed_and_departed_flights_by_airline()

    percentage_of_delayed_flights = []
    airline = []

    for flight_data in flights_data:
        try:
            percentage_of_delayed_flights.append(
                (flight_data['num_of_delayed_flights'] / flight_data['num_of_flights']) * 100)
            airline.append(flight_data['AIRLINE'])

        except (ValueError, sqlalchemy.exc.SQLAlchemyError) as e:
            print("Error showing results: ", e)
            return
    # visualize the result
    visualize_data_result(airline, percentage_of_delayed_flights, visual_type='bar_chart')


def percentage_of_delayed_flights_by_hour_of_day(data_manager):
    """
    When selected by the user. This function gets the delay and departure time for each flight.
    This data will be used to calculate the percentage of delayed flights for each hour of the day.
    If no exception errors, it parses the results to the visualize data result function
    to display the chart plot to the user. The visual_type is also specified.
    """
    # Gets flight details
    flights_data = data_manager.get_delay_and_departure_time()

    departure_delay = []
    departure_time = []

    for flight_data in flights_data:
        try:
            departure_delay.append(flight_data['DELAY'])
            departure_time.append(int(flight_data['DEPARTURE_TIME'][:2]))

        except (ValueError, sqlalchemy.exc.SQLAlchemyError) as e:
            print("Error showing results: ", e)
            return

    # Visualize the data
    visualize_data_result(departure_delay, departure_time, visual_type='bar_chart_with_colorbar')


def percentage_of_delay_for_routes(data_manager):
    """
    When selected by the user. This function gets the origin airport, destination airport
    and percentage delay for each flight route.
    If no exception errors, it parses the results to the visualize data result function
    to display the chart plot to the user. The visual_type is also specified.
    """
    # Gets flight data
    flights_data = data_manager.get_origin_destination_airport_delay()

    origin_airport = []
    destination_airport = []
    percent_delay_per_route = []

    for flight_data in flights_data:
        try:
            origin_airport.append(flight_data['ORIGIN_AIRPORT'])
            destination_airport.append(flight_data['DESTINATION_AIRPORT'])
            percent_delay_per_route.append(flight_data['percentage_delay'])

        except (ValueError, sqlalchemy.exc.SQLAlchemyError) as e:
            print("Error showing results: ", e)
            return
    # Visualize data
    visualize_data_result(origin_airport, destination_airport, percent_delay_per_route,
                          visual_type='heat_map')


def percentage_delayed_flights_per_route_on_map(data_manager):
    """
    When selected by the user. This function gets the origin airport and origin airport coordinate as well as
    destination airport and destination airport coordinate and finally the percentage delay per route.
    The data is used to plot flight routes on the map and the percentage delay is shown on the line plots.
    If no exception errors, it parses the results to the visualize data result function
    to display the chart plot to the user. The visual_type is also specified.
    """
    # Gets Flight data
    flights_data = data_manager.get_origin_destination_latitude_longitude()

    origin_airport = []
    origin_airport_latitude = []
    origin_airport_longitude = []

    destination_airport = []
    destination_airport_latitude = []
    destination_airport_longitude = []

    percent_delay_per_route = []

    for flight_data in flights_data:
        try:
            origin_airport.append(flight_data['origin_airport'])
            origin_airport_longitude.append(float(flight_data['origin_longitude']))
            origin_airport_latitude.append(float(flight_data['origin_latitude']))
            destination_airport.append(flight_data['destination_airport'])
            destination_airport_longitude.append(float(flight_data['destination_longitude']))
            destination_airport_latitude.append(float(flight_data['destination_latitude']))
            percent_delay_per_route.append(flight_data['percentage_delay'])

        except (ValueError, sqlalchemy.exc.SQLAlchemyError) as e:
            print("Error showing results: ", e)
            return

    # Visulaize data result
    visualize_data_result(origin_airport, origin_airport_longitude, origin_airport_latitude, destination_airport,
                          destination_airport_longitude, destination_airport_latitude, percent_delay_per_route,
                          visual_type='route_map')


def print_results(results):
    """
    Get a list of flight results (List of dictionary-like objects from SQLAachemy).
    Even if there is one result, it should be provided in a list.
    Each object *has* to contain the columns:
    FLIGHT_ID, ORIGIN_AIRPORT, DESTINATION_AIRPORT, AIRLINE, and DELAY.
    """
    print(f"Got {len(results)} results.")
    for result in results:
        # Check that all required columns are in place
        try:
            delay = int(result['DELAY']) if result['DELAY'] else 0  # If delay columns is NULL, set it to 0
            origin = result['ORIGIN_AIRPORT']
            dest = result['DESTINATION_AIRPORT']
            airline = result['AIRLINE']
        except (ValueError, sqlalchemy.exc.SQLAlchemyError) as e:
            print("Error showing results: ", e)
            return

        # Different prints for delayed and non-delayed flights
        if delay and delay > 0:
            print(f"{result['ID']}. {origin} -> {dest} by {airline}, Delay: {delay} Minutes")
        else:
            print(f"{result['ID']}. {origin} -> {dest} by {airline}")


def visualize_data_result(*args, visual_type):
    """
    This function calls the appropriate function (value) to execute a data visualization
    based on the specified visual type (key)
    """
    visual_method = {
        'bar_chart': plot_bar_chart,
        'bar_chart_with_colorbar': plot_bar_chart_with_colorbar,
        'heat_map': plot_heat_map,
        'route_map': plot_route_map
    }

    visual_method[visual_type](args)

def quit_app(data_manager):
    """
    Exits the User from the application
    :param args: data_manager object
    :return: None
    """
    print("\033[1;37m Bye! \033[0m")
    quit()


def show_menu_and_get_input():
    """
    Show the menu and get user input.
    If it's a valid option, return a pointer to the function to execute.
    Otherwise, keep asking the user for input.
    """
    print("Menu:")
    for key, value in FUNCTIONS.items():
        print(f"{key}. {value[1]}")

    # Input loop
    while True:
        try:
            choice = int(input())
            if choice in FUNCTIONS:
                return FUNCTIONS[choice][0]
        except ValueError as e:
            pass
        print("Try again...")


"""
Function Dispatch Dictionary
"""
FUNCTIONS = {1: (flight_by_id, "Show flight by ID"),
             2: (flights_by_date, "Show flights by date"),
             3: (delayed_flights_by_airline, "Delayed flights by airline"),
             4: (delayed_flights_by_airport, "Delayed flights by origin airport"),
             5: (percentage_of_delayed_flights_per_airline, 'Display percentage of delayed flights by airline'),
             6: (percentage_of_delayed_flights_by_hour_of_day, 'Display percentage of delayed flights per hour of the day'),
             7: (percentage_of_delay_for_routes,
                 'Display percentage of delayed heatmap for each route origin airport -> destination airport'),
             8: (percentage_delayed_flights_per_route_on_map,
                 'Display Map Plot of percentage of delayed flights per route'),
             9: (quit_app, "Exit")
             }


def main():
    # Create an instance of the Data Object using our SQLite URI
    data_manager = data.FlightData(SQLITE_URI)

    # The Main Menu loop
    while True:
        choice_func = show_menu_and_get_input()
        choice_func(data_manager)


if __name__ == "__main__":
    main()
