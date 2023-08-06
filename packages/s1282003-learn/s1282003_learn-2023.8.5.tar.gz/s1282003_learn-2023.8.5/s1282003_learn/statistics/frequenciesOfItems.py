class frequenciesOfItems:
    """
    A class used to count the frequency of each sensor point from the provided relational database.

    Attributes
    ----------
    filename
        the name of the relational database file
    separator
        the separator used in the relational database file

    Methods
    -------
    __init__(filename, separator)
        the constructor of the frequenciesOfItems class
    process_file()
        function to open the file, read through them, and count the frequency of each sensor point.
    """

    def __init__(self, filename, separator):
        """
        The constructor of the frequenciesOfItems class

        Parameters
        ----------
        filename
            the name of the relational database file
        separator
            the separator used in the relational database file
        """

        self.filename = filename
        self.separator = separator

    def process_file(self):
        """
        A function used to open the relational database file, read the file, and count the frequency of each sensor point in the file. Then, return the frequency count as a dictionary.

        Returns
        -------
        frequencies_dict
            a dictionary containing the sensor point as key, and the frequency of the corresponding point as the value
        """

        # Initialize an empty dictionary to store the frequencies of points
        frequencies_dict = {}

        try:
            with open(self.filename, "r") as file:
                # Read each line in the file
                for line in file:
                    # Split the line using the given separator to get individual points
                    points = line.strip().split(self.separator)

                    # Count the frequency of each point and update the dictionary
                    for point in points:
                        if point not in frequencies_dict:
                            frequencies_dict[point] = 1
                        else:
                            frequencies_dict[point] += 1

        except FileNotFoundError:
            print(f"File '{self.filename}' not found.")
            return None

        return frequencies_dict
