import ast


def to_dict_convertor(x: str):
    """
    Converts a string representation of a Python literal (e.g., a dictionary)
    into its corresponding Python object. If the conversion fails, returns None.

    Args:
        x (str): The string to be converted.

    Returns:
        dict or None: The converted Python object if successful, otherwise None.
    """
    try:
        return ast.literal_eval(
            x
        )  # try to evaluate the string as a python literal (e.g., dict)
    except:
        return None
