import pandas as pd
import plotly.express as px

class HeatMapItemsFrequencies:
    """
    A class to calculate item frequencies from a transactional database and plot a heatmap
    of the item frequencies on an OpenStreetMap using Plotly Express.
    
    ...

    Attributes
    ----------
    database : str
        The filename of the transactional database.
    separator : str, optional
        The separator used in the transactional database file. Default is tab '\t'.
    item_freq : dict
        A dictionary to store the calculated item frequencies.

    Methods
    -------
    calculate_frequencies()
        Calculates item frequencies from the transactional database file.
        
    get_frequencies()
        Returns the calculated item frequencies as a dictionary where the keys are the items
        and the values are their frequencies.
        
    plot_heatmap(data)
        Plots the heatmap of item frequencies on an OpenStreetMap using Plotly Express.
        Requires a dictionary `data` where the keys are the items and the values are their frequencies.
    """
    
    def __init__(self, database, separator='\t'):
        """
        Initializes the HeatMapItemsFrequencies object.

        Parameters
        ----------
        database : str
            The filename of the transactional database.
        separator : str, optional
            The separator used in the transactional database file. Default is tab '\t'.
        """
        self.database = database
        self.separator = separator
        self.item_freq = {}

    def calculate_frequencies(self):
        """
        Calculate item frequencies from the transactional database file.

        The calculated frequencies are stored in the `item_freq` attribute of the object.
        """
        with open(self.database, 'r') as file:
            for line in file:
                items = line.strip().split(self.separator)
                for item in items:
                    if item in self.item_freq:
                        self.item_freq[item] += 1
                    else:
                        self.item_freq[item] = 1

    def get_frequencies(self):
        """
        Get the calculated item frequencies.

        Returns
        -------
        dict
            A dictionary where the keys are the items and the values are their frequencies.
        """
        return self.item_freq

    def plot_heatmap(self, data):
        """
        Plot the heatmap of item frequencies on an OpenStreetMap.

        Parameters
        ----------
        data : dict
            A dictionary where the keys are the items and the values are their frequencies.
        """
        # Extract latitude, longitude, and count from the data dictionary
        latitude = []
        longitude = []
        count = []
        for point, freq in data.items():
            # Remove 'POINT(' and ')' from the point
            point = point.replace('POINT(', '').replace(').1', '').replace(')', '')
            lon, lat = point.split(' ')  # Extract longitude and latitude from the point
            longitude.append(float(lon))
            latitude.append(float(lat))
            count.append(freq)

        # Create a DataFrame with the extracted values
        df = pd.DataFrame({'latitude': latitude, 'longitude': longitude, 'count': count})

        # Create a heatmap on an OpenStreetMap using Plotly Express
        fig = px.density_mapbox(df, lat='latitude', lon='longitude', z='count',
                                radius=10, center={'lat': 34.686567, 'lon': 135.52000},
                                mapbox_style='open-street-map',
                                zoom=4, height=600, width=800)

        # Show the heatmap
        fig.show()

# Example usage:
if __name__ == "__main__":
    # Assuming 'PM24HeavyPollutionRecordingSensors.csv' is your transactional database file name
    transactional_db = 'PM24HeavyPollutionRecordingSensors.csv'
    separator = '\t'

    # Create the HeatMapItemsFrequencies object and calculate frequencies
    items_frequencies = HeatMapItemsFrequencies(transactional_db, separator)
    items_frequencies.calculate_frequencies()

    # Get the frequency dictionary
    items_freq_dictionary = items_frequencies.get_frequencies()

    # Plot the heatmap
    items_frequencies.plot_heatmap(items_freq_dictionary)