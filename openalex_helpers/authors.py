import pandas as pd
import requests
from pyalex import Authors


def get_authors_by_name_and_rors(name: str, ror_ids: list[str]):
    """
    Fetch author details from the OpenAlex API by name and a list of affiliated ROR IDs.

    Args:
        name (str): The name of the author.
        ror_ids (list[str]): A list of ROR IDs associated with the author.

    Returns:
        pandas.DataFrame: A pandas DataFrame containing authors matching the name and ROR IDs.
    """
    json_data = (
        Authors()
            .search(name)
            .filter_or(affiliations={
                "institution": {
                    "ror": ror_ids
                }
            })
            .get()
    )
    df = pd.DataFrame(json_data)

    return df
