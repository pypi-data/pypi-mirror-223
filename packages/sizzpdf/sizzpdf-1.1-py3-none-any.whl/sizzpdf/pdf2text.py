""" This is a module to convert pdf to text.

    Something others.
"""


class Convert:
    """ A simple convert for pdf to text.
    """

    def convert(self, path):
        """ This function read a pdf from path and convert it to text.

        Parameters:
        path (str) : a path to pdf file.

        Returns:
        str : the content of the pdf file as text.
        """
        print(f"{path} to text.")
