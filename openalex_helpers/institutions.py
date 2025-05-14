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
    # construct the api url with the given ror id
    url = f"https://api.openalex.org/institutions?filter=ror:{ror_id}"

    # send a GET request to the api and parse the json response
    response = requests.get(url)
    json_data = response.json()

    # convert the json response to a dataframe
    df_json = pd.DataFrame.from_dict(json_data["results"])

    return df_json.iloc[0]
