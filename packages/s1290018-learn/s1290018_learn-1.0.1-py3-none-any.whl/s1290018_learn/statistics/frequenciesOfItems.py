class FrequenciesOfItems:
    """
    A class to calculate item frequencies from a transactional database.

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
        Calculates item frequencies from the transactional database file and stores them in the `item_freq` attribute.
        
    get_frequencies()
        Returns the calculated item frequencies as a dictionary where the keys are the items
        and the values are their frequencies.
    """
    
    def __init__(self, database, separator='\t'):
        """
        Initializes the FrequenciesOfItems object.

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

# Example usage:
if __name__ == "__main__":
    # Assuming 'PM24HeavyPollutionRecordingSensors.csv' is your transactional database file name
    transactional_db = 'PM24HeavyPollutionRecordingSensors.csv'
    separator = '\t'

    # Create the FrequenciesOfItems object and calculate frequencies
    items_frequencies = FrequenciesOfItems(transactional_db, separator)
    items_frequencies.calculate_frequencies()

    # Get the frequency dictionary
    items_freq_dictionary = items_frequencies.get_frequencies()

    print(items_freq_dictionary)