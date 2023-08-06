import numpy as np
import pandas as pd
from matplotlib import pyplot as plt
from matplotlib.cm import ScalarMappable
from matplotlib.colors import Normalize


def plot_bar_chart(args):
    """
    plots a bar chart showing percentage of delay per airline and shows it to the user
    :param args: airline, percentage of delayed flights per airline
    :return: None
    """
    # Unpack args
    airline, percentage_of_delayed_flights = args

    # Sets the plot size window
    plt.figure(figsize=(10, 6))

    # create bar chart
    plt.bar(airline, percentage_of_delayed_flights, color='#2596be')

    # Set y-axis ticks interval to range from 0 to max-num + 5.
    # Set regular intervals of 5. Bold font and font size of 9
    plt.yticks(range(0, int(max(percentage_of_delayed_flights)) + 5, 5), fontsize=9, weight='bold')

    # Get the range of all the x-label,
    # align labels to the right of the bar chart
    # Rotate the x-axis labels at a 30-degree angle
    plt.xticks(range(len(airline)), airline, rotation=30, ha='right', fontsize=9, weight='bold')

    # Add labels and title
    plt.xlabel('Airline', fontsize=14, weight='bold')
    plt.ylabel('Percentage of Delayed Flights', weight='bold')
    plt.title('Percentage of Delayed Flights by Airline', weight='bold')

    # Ensures that no label is cut off and displays everything nicely
    plt.tight_layout()

    # Show the plot
    plt.show()


def plot_bar_chart_with_colorbar(args):
    """
     plots a bar chart with color bar on the side of percentage delay for every hour of the day.
     shows the plot to the user
    :param args: departure delay (in minutes), departure time (in hours)
    :return: None
    """
    # Flight data_db: (departure_delay in minutes; departure_time in hours)
    departure_delay, departure_time = args

    flight_data = {
        'DEPARTURE_DELAY': departure_delay,
        'HOUR_OF_DAY': departure_time
    }

    # Convert the flight data_db to a pandas DataFrame (df)
    df = pd.DataFrame(flight_data)

    # Get counts for number of delays per hour of the day.
    # E.g Hour 15 had 5 delays, Hour 5 had 3 delays, Hour 8 had 15 delays, etc..
    # Sort the index. The index here is the hours in which the delay occurred.
    delayed_flights_per_hour = df['HOUR_OF_DAY'].value_counts().sort_index()

    # Calculate the total number of flights by summing up the counts of delay per hour of the day.
    total_flights = delayed_flights_per_hour.sum()

    # Calculate the percentage of delayed flights per hour of the day
    percentage_delayed_per_hour = (delayed_flights_per_hour / total_flights) * 100

    # Create a colormap for the bar chart
    colormap = plt.cm.viridis

    # Create the figure and axes for the bar chart
    fig, ax = plt.subplots(figsize=(10, 6))

    # Create the bar chart
    bars = ax.bar(percentage_delayed_per_hour.index, percentage_delayed_per_hour.values,
                  color=colormap(percentage_delayed_per_hour.values / 10))

    # Create the legend colorbar using the ScalarMappable object
    sm = plt.cm.ScalarMappable(cmap=colormap, norm=plt.Normalize(vmin=0, vmax=10))
    sm.set_array(percentage_delayed_per_hour.values)  # Set the array to map the colors correctly
    cbar = plt.colorbar(sm, ax=ax)
    cbar.set_label('Percentage Delayed')  # Label for the colorbar

    # Set x-axis ticks interval to range from 1 to 25.
    plt.xticks(range(0, 25))

    # Add labels and title
    plt.xlabel('Hour of the Day')
    plt.ylabel('Percentage Delayed')
    plt.title('Percentage of Delayed Flights per Hour of the Day')

    # Show the plot
    plt.tight_layout()
    plt.show()


def plot_heat_map(args):
    """
     plots the percentage of delay for each route on a heat map. Displays it to the user
    :param args: origin airport, destination airport, percentage of delay for routes
    :return: None
    """
    # Unpacking the args
    origin_airport, destination_airport, percentage_of_delay_for_routes = args

    data = {
        'origin': origin_airport,
        'destination': destination_airport,
        'percentage_delay': percentage_of_delay_for_routes,
    }

    # Convert data_db to a pandas dataframe (df)
    df = pd.DataFrame(data)

    # Randomly sample 500 data_db points.
    # Random_state is set at 42 to maintain a constant random selection each time
    sampled_df = df.sample(n=500, random_state=42)

    # Create a pivot table to convert the sampled data_db into a 2D array.
    # This makes origin the index, destination the column and percentage delay the data.
    # Thus making it easier to make comparison and plot the heat map
    heatmap_data = pd.pivot_table(sampled_df, values='percentage_delay', index='origin', columns='destination')

    # Convert the pivot table to a 2D numpy array
    percentage_delay_array = heatmap_data.to_numpy()

    # Replace nan values with 0 on both axes
    np.nan_to_num(percentage_delay_array, nan=0.0, copy=False)

    fig, ax = plt.subplots(figsize=(10, 7))

    # Use a diverging color map for better visibility
    # Color can be found here https://matplotlib.org/stable/tutorials/colors/colormaps.html
    cmap = 'plasma'

    # Plots the heat map
    # Set the aspect ratio to 'equal'
    im = ax.imshow(percentage_delay_array, cmap=cmap, aspect='equal')

    # Adding color bar legend to the Heatmap
    cbar = ax.figure.colorbar(im, ax=ax, shrink=0.7)

    # Setting the axis tick values and labels
    ax.set_yticks(np.arange(len(heatmap_data.index)))
    ax.set_xticks(np.arange(len(heatmap_data.columns)))

    ax.set_yticklabels(heatmap_data.index, rotation=0, fontsize=8)
    ax.set_xticklabels(heatmap_data.columns, rotation=90, fontsize=8)

    ax.set_title("Percentage of delayed on a heatmap of routes (Origin <-> Destination)")

    # show chart
    plt.tight_layout()
    plt.show()


def plot_route_map(args):
    """
    Plots the flight routes on a map image with .png format. The the percentage delay is represented
    with intensity colours on the route lines that connects origin and destination airports.
    :param args: origin airport and coordinate, destination airport and coordinate, percentage delay
    :return:
    """
    # Unpacking the args
    origin, origin_long, origin_lat, destination, destination_long, destination_lat, percentage_delay = args

    data = {
        'origin': origin,
        'origin_longitude': origin_long,
        'origin_latitude': origin_lat,
        'destination': destination,
        'destination_longitude': destination_long,
        'destination_latitude': destination_lat,
        'percentage_delay': percentage_delay,
    }

    # Convert data_db to a pandas dataframe (df)
    df = pd.DataFrame(data)

    # Randomly sample 50 data_db points
    sampled_df = df.sample(n=50, random_state=42)

    # define map extent. Give map extent an allowance of 0.5 to display plot nicely
    map_extent = [sampled_df.origin_longitude.min() - 0.5, sampled_df.origin_longitude.max() + 0.5,
                  sampled_df.origin_latitude.min() - 0.5, sampled_df.origin_latitude.max() + 0.5]

    # read the map image
    img_map = plt.imread('map.png')

    # Create the plot and set the figure size
    fig, ax = plt.subplots(figsize=(8, 4))

    # Setting limits for the plot
    ax.set_xlim(map_extent[0], map_extent[1])
    ax.set_ylim(map_extent[2], map_extent[3])

    # Plot the image map
    ax.imshow(img_map, extent=map_extent, aspect='equal')

    # Normalize the percentage_delay values to fit within the colormap range (0 to 1)
    norm = Normalize(vmin=sampled_df['percentage_delay'].min(), vmax=sampled_df['percentage_delay'].max())
    sampled_df['normalized_percentage_delay'] = norm(sampled_df['percentage_delay'])

    # Color range that is used to display the intensity
    cmap = 'viridis'

    # Plot the airports as points with different shades of color intensity based on average delay
    for _, row in sampled_df.iterrows():
        color = plt.get_cmap(cmap)(row['normalized_percentage_delay'])
        ax.plot([row['origin_longitude'], row['destination_longitude']],
                [row['origin_latitude'], row['destination_latitude']], 'o', markersize=4, color=color)

    # Draw lines connecting the origin and destination airports
    for _, row in sampled_df.iterrows():
        color = plt.get_cmap(cmap)(row['normalized_percentage_delay'])
        ax.plot([row['origin_longitude'], row['destination_longitude']],[row['origin_latitude'], row['destination_latitude']], '-', color=color)

    # Create ScalarMappable to add color bar
    sm = ScalarMappable(cmap=cmap, norm=norm)
    sm.set_array([])  # Set empty array to correctly map the colors

    # Add color bar. Set color bar orientation and aspect including padding
    cbar = plt.colorbar(sm, ax=ax, orientation='horizontal', shrink=0.3, aspect=30, pad=0.1)
    cbar.set_label('Percentage Delay')
    cbar.ax.tick_params(length=0)

    # Show the plot
    plt.title('Percentage of Delayed Flights per Route (Both Directions Average)')
    plt.show()