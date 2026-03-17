from pyalex import Institutions

import pandas as pd
import requests


def get_institution_by_ror(ror_id: str):
    """
    Fetch institution details from the OpenAlex API by ROR ID.

    Args:
        ror_id (str): The ROR ID of the institution.

    Returns:
        pandas.Series: A pandas Series containing the first result for the specified ROR ID.
    """
    json_data = Institutions().filter(ror=ror_id).get()
    df = pd.DataFrame(json_data)

    return df.iloc[0]