import pandas as pd
import requests


def get_authors_by_name_and_rors(name: str, ror_ids: list[str]):
    """
    Fetch author details from the OpenAlex API by name and a list of affiliated ROR IDs.

    Args:
        name (str): The name of the author.
        ror_ids (list[str]): A list of ROR IDs associated with the author.

    Returns:
        pandas.DataFrame: A pandas DataFrame containing authors matching the name and ROR IDs.
    """
    # construct the api url with the given author's name and ror ids
    url = f"https://api.openalex.org/authors?search={name}&filter=affiliations.institution.ror:{'|'.join(ror_ids)}"

    # send a GET request to the api and parse the json response
    response = requests.get(url)
    json_data = response.json()

    # convert the json response to a dataframe
    df_json = pd.DataFrame.from_dict(json_data["results"])

    return df_json
