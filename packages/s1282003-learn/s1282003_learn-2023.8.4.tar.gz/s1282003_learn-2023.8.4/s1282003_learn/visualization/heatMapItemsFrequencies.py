import plotly.express as px
from s1282003_learn.statistics.frequenciesOfItems import frequenciesOfItems


class HeatMapItemsFrequencies:
    """
    A class to create a heatmap of item frequencies at specific geographical coordinates.

    Attributes
    ----------
    filename
        The name of the CSV file containing the transactional database.
    separator
        The separator used in the CSV file to separate values.

    Methods
    -------
    __init__(filename, separator)
        Initializes the HeatMapItemsFrequencies class with the given CSV filename and separator.
    extract_coordinates_from_point(point_str)
        Extracts latitude and longitude coordinates from the given point string.
    process_file()
        Processes the CSV file and gets the items frequencies dictionary.
    plot_heatmap()
        Plots a heatmap using Plotly Express based on the items frequencies dictionary.
    """

    def __init__(self, filename, separator):
        """
        Initializes the HeatMapItemsFrequencies class.

        Parameters
        ----------
        filename
            The name of the CSV file containing transactional database.
        separator
            The separator used in the CSV file to separate values.
        """

        self.filename = filename
        self.separator = separator

    def extract_coordinates_from_point(self, point_str):
        """
        Extracts latitude and longitude coordinates from the given point string in the frequency dictionary.

        Parameters
        ----------
        point_str
            The point string obtained from the frequency dictionary.

        Returns
        -------
        coordinates
            A list of tuples containing latitude and longitude coordinates.
        """

        # Separate each points and extract the coordinates
        points = point_str.split("\t")
        coordinates = []
        for point in points:
            lon, lat = map(float, point[6:-3].split())
            coordinates.append((lon, lat))
        return coordinates

    def process_file(self):
        """
        Use the frequenciesOfItem class to process the transactional database and gets the items frequencies dictionary.

        Returns
        -------
        items_frequencies_dict
            A dictionary containing items as keys and their corresponding frequencies as values.
        """

        # Call the process_file() method of the frequenciesOfItems class to get the output dictionary
        items_frequencies_dict = frequenciesOfItems(
            self.filename, self.separator
        ).process_file()
        return items_frequencies_dict

    def plot_heatmap(self):
        """
        Plots a heatmap using Plotly Express based on the items frequencies dictionary.
        """

        # Call the process_file() method to get the output dictionary
        items_frequencies_dict = self.process_file()

        if items_frequencies_dict is not None:
            # Extract latitude and longitude from the dictionary keys
            latitudes = []
            longitudes = []
            frequencies = []

            for point, frequency in items_frequencies_dict.items():
                # Extracting the latitude and longitude values from the point string
                coordinates = self.extract_coordinates_from_point(point)
                for lon, lat in coordinates:
                    longitudes.append(lon)
                    latitudes.append(lat)
                    frequencies.append(frequency)

            # Create a DataFrame to be used by Plotly Express
            import pandas as pd

            data = pd.DataFrame(
                {
                    "Latitude": latitudes,
                    "Longitude": longitudes,
                    "Frequency": frequencies,
                }
            )

            # Create a heatmap on an OpenStreetMap using Plotly Express
            fig = px.density_mapbox(
                data,
                lat="Latitude",
                lon="Longitude",
                z="Frequency",
                radius=10,
                center={"lat": 36.686567, "lon": 135.52000},
                zoom=3.8,
                height=600,
                width=800,
                mapbox_style="open-street-map",
            )

            # Show the plot
            fig.show()

        else:
            print("Error occurred while processing the file.")


if __name__ == "__main__":
    filename = "PM24HeavyPollutionRecordingSensors.csv"
    separator = "\t"
    heatmap = HeatMapItemsFrequencies(filename, separator)
    heatmap.plot_heatmap()
