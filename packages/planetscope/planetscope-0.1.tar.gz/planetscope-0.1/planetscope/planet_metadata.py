"""
Module containing a third class.
"""

import numpy as np
from xml.dom import minidom
import pandas as pd

def check_xmlfile_type(xml_filename):
    """
    Check the type of input XML file and parse it if necessary.

    This function checks the type of the input `xml_filename` and performs parsing if required.
    It accepts either a `Document` object or a file path to the XML file in string format.

    Args:
        xml_filename (str or xml.dom.minidom.Document): The input XML filename or Document object.

    Returns:
        xml.dom.minidom.Document: The parsed XML Document object.

    Raises:
        IOError: If the input data is of the wrong type.

    Example:
        The following examples illustrate how to use the `check_xmlfile_type` function:

        1. Input is a string representing the file path:
        
        .. code-block:: python
        
            xml_file_path = "path/to/your/xml_file.xml"
            parsed_xml = check_xmlfile_type(xml_file_path)

        2. Input is an existing XML Document object:

        .. code-block:: python

            from xml.dom import minidom
            xml_document = minidom.parseString("<root><element>Value</element></root>")
            parsed_xml = check_xmlfile_type(xml_document)
    """
    if isinstance(xml_filename, minidom.Document):
        # If the input is already an XML Document, no parsing is needed
        xml_parsed = xml_filename
    elif isinstance(xml_filename, str):
        # If the input is a string representing the file path, parse the XML file
        xml_parsed = minidom.parse(xml_filename)
    else:
        # If the input is of the wrong type, raise an error
        raise IOError("Wrong type of input data")

    return xml_parsed


def get_coeffs(xml_filename):
    """
    Extract coefficients for converting digital numbers (DN) to reflectance from PlanetScope XML metadata.

    This function parses the provided PlanetScope XML file to extract band-specific metadata, including
    the coefficients required for converting DN to reflectance. It returns a dictionary containing the
    band number (1 to 4) as keys and the corresponding reflectance coefficients as values.

    Args:
        xml_filename (str or xml.dom.minidom.Document): The input XML filename or Document object.

    Returns:
        dict: A dictionary containing band numbers (1 to 4) as keys and their respective reflectance coefficients as values.

    Example:
        The following example demonstrates how to use the `get_coeffs` function:

        .. code-block:: python

            from xml.dom import minidom

            # Example 1: Input is a string representing the file path
            xml_file_path = "path/to/your/xml_file.xml"
            coeffs_dict = get_coeffs(xml_file_path)

            # Example 2: Input is an existing XML Document object
            xml_document = minidom.parseString("<root><ps:bandSpecificMetadata><ps:bandNumber>1</ps:bandNumber><ps:reflectanceCoefficient>0.2</ps:reflectanceCoefficient></ps:bandSpecificMetadata></root>")
            coeffs_dict = get_coeffs(xml_document)

        The resulting `coeffs_dict` will contain the reflectance coefficients for bands 1 to 4, if available in the XML metadata.
    """
    # Parse the XML file if needed
    xml_parsed = (
        xml_filename
        if isinstance(xml_filename, minidom.Document)
        else minidom.parse(xml_filename)
    )

    # Extract band-specific metadata nodes from the XML
    nodes = xml_parsed.getElementsByTagName("ps:bandSpecificMetadata")

    # Initialize a dictionary to store band number (1 to 4) as keys and their corresponding reflectance coefficients as values
    coeffs = {}

    # Loop through the metadata nodes and extract coefficients for bands 1 to 4
    for node in nodes:
        bn = node.getElementsByTagName("ps:bandNumber")[0].firstChild.data
        if bn in ["1", "2", "3", "4"]:
            i = int(bn)
            value = node.getElementsByTagName("ps:reflectanceCoefficient")[0].firstChild.data
            coeffs[i] = float(value)

    return coeffs


def extract_element(corner):
    """
    Extract longitude and latitude coordinates for a specified corner from PlanetScope XML metadata.

    This function extracts the longitude and latitude coordinates for a specified corner (e.g., 'upperRight',
    'upperLeft', 'lowerRight', 'lowerLeft') from the provided PlanetScope XML metadata. The coordinates are
    returned as a list with longitude at index 0 and latitude at index 1.

    Args:
        corner (str): The corner for which longitude and latitude coordinates are to be extracted.

    Returns:
        list: A list containing the longitude and latitude coordinates for the specified corner.

    Example:
        The following example demonstrates how to use the `extract_element` function:

        .. code-block:: python

            from xml.dom import minidom

            # Example: Extract coordinates for the 'upperRight' corner
            xml_document = minidom.parseString("<root><ps:upperRight><ps:longitude>25.1234</ps:longitude><ps:latitude>50.5678</ps:latitude></ps:upperRight></root>")
            corner_coordinates = extract_element('upperRight')

            # Output: corner_coordinates = [25.1234, 50.5678]
        
        The resulting `corner_coordinates` list will contain the longitude and latitude coordinates for the specified corner.
    """
    # Define the XML tag names for longitude and latitude
    tags = ["longitude", "latitude"]

    # Construct the XML tag names for the specified corner
    corner_tags = ["ps:" + corner] * len(tags)

    # Extract the longitude and latitude coordinates from the XML metadata
    coordinates = [
        location.getElementsByTagName(tag)[0].firstChild.data
        for tag, location in zip(corner_tags, np.array(tags))
    ]

    return coordinates


def get_location(xml_filename):
    """
    Extract geographic locations for the bounding box corners from PlanetScope XML metadata.

    This function parses the provided PlanetScope XML file to extract geographic locations (longitude and latitude)
    for the bounding box corners, namely 'topLeft', 'topRight', 'bottomLeft', and 'bottomRight'. The locations are 
    returned as a Pandas DataFrame, with columns representing longitude and latitude, and rows representing the
    bounding box corners (TL for topLeft, TR for topRight, BL for bottomLeft, and BR for bottomRight).

    Args:
        xml_filename (str or xml.dom.minidom.Document): The input XML filename or Document object.

    Returns:
        pandas.DataFrame: A DataFrame containing geographic locations for the bounding box corners.

    Example:
        The following example demonstrates how to use the `get_location` function:

        .. code-block:: python

            from xml.dom import minidom
            import pandas as pd

            # Example 1: Input is a string representing the file path
            xml_file_path = "path/to/your/xml_file.xml"
            location_df = get_location(xml_file_path)

            # Example 2: Input is an existing XML Document object
            xml_document = minidom.parseString("<root><ps:geographicLocation><ps:topLeft><ps:longitude>25.1234</ps:longitude><ps:latitude>50.5678</ps:latitude></ps:topLeft><ps:topRight><ps:longitude>26.9876</ps:longitude><ps:latitude>51.3456</ps:latitude></ps:topRight><ps:bottomLeft><ps:longitude>24.6789</ps:longitude><ps:latitude>49.8765</ps:latitude></ps:bottomLeft><ps:bottomRight><ps:longitude>27.5432</ps:longitude><ps:latitude>52.1234</ps:latitude></ps:bottomRight></ps:geographicLocation></root>")
            location_df = get_location(xml_document)

        The resulting `location_df` DataFrame will contain the geographic locations for the bounding box corners.
    """
    # Parse the XML file if needed
    xml_parsed = (
        xml_filename
        if isinstance(xml_filename, minidom.Document)
        else minidom.parse(xml_filename)
    )

    # Extract the 'ps:geographicLocation' node from the XML
    location = xml_parsed.getElementsByTagName("ps:geographicLocation")

    # Extract geographic locations for the bounding box corners
    tl = extract_element("topLeft")
    tr = extract_element("topRight")
    bl = extract_element("bottomLeft")
    br = extract_element("bottomRight")

    # Convert the locations to a Pandas DataFrame
    bounding_boxes = np.array([tl, tr, bl, br])
    location_df = pd.DataFrame(
        bounding_boxes, columns=["lon", "lat"], index=["TL", "TR", "BL", "BR"]
    )

    return location_df

