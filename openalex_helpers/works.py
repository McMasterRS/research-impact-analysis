from typing import List

import pandas as pd
import requests


def get_works_by_dois(dois: List[str], page: int = 1, items_per_page: int = 50):
    """
    Fetch works from the OpenAlex API for the given DOIs.

    This function queries the OpenAlex API for works associated with one or
    more DOIs. If additional pages are available, it recursively fetches them
    and concatenates them into a single pandas DataFrame.

    Args:
        dois (List[str]): A list of DOIs for which to retrieve works.
        page (int, optional): The current page number for pagination. Defaults to 1.
        items_per_page (int, optional): Number of records per page. Defaults to 50.

    Returns:
        pd.DataFrame: A DataFrame containing the works retrieved for the specified DOIs.
    """
    # construct the api url with the given dois, page number, and items per page
    url = (
        "https://api.openalex.org/works?"
        f"filter=doi:{'|'.join(dois)}"
        f"&page={page}&per-page={items_per_page}"
    )

    # send a GET request to the api and parse the json response
    response = requests.get(url)
    json_data = response.json()

    # convert the json response to a dataframe
    df_json = pd.DataFrame.from_dict(json_data["results"])

    next_page = (
        not df_json.empty
    )  # check if the dataframe is empty (i.e., no more pages available)
    # if there are more pages, recursively fetch the next page
    if next_page:
        df_json_next_page = get_works_by_dois(
            dois, page=page + 1, items_per_page=items_per_page
        )
        df_json = pd.concat([df_json, df_json_next_page])

    return df_json


def get_works_by_author(author_id: str, page: int = 1, items_per_page: int = 50):
    """
    Fetch works from the OpenAlex API for a specified author.

    Args:
        author_id (str): The ID of the author.
        page (int, optional): The current page number for pagination. Defaults to 1.
        items_per_page (int, optional): Number of records per page. Defaults to 50.

    Returns:
        pd.DataFrame: A DataFrame containing the works retrieved for the specified author.
    """
    # construct the api url with the given author id, page number, and items per page
    url = (
        "https://api.openalex.org/works?"
        f"filter=author.id:{author_id}"
        f"&page={page}&per-page={items_per_page}"
    )

    # send a GET request to the api and parse the json response
    response = requests.get(url)
    json_data = response.json()

    # convert the json response to a dataframe
    df_json = pd.DataFrame.from_dict(json_data["results"])

    next_page = (
        not df_json.empty
    )  # check if the dataframe is empty (i.e., no more pages available)
    # if there are more pages, recursively fetch the next page
    if next_page:
        df_json_next_page = get_works_by_author(
            author_id, page=page + 1, items_per_page=items_per_page
        )
        df_json = pd.concat([df_json, df_json_next_page])

    return df_json


def get_works_by_corresponding_institutions(
    institution_ids: List[str],
    publication_year: int,
    publication_types: List[str],
    publication_oa_statuses: List[str],
    page: int = 1,
    items_per_page: int = 50,
):
    """
    Fetches works from the OpenAlex API for corresponding institutions, year, publication types, and OA statuses.

    Args:
        institution_ids (List[str]): The IDs of the corresponding institution.
        publication_year (int): The publication year to filter by.
        publication_types (List[str]): Types of publications to include.
        publication_oa_statuses (List[str]): Open access statuses to include.
        page (int, optional): The current page number for pagination. Defaults to 1.
        items_per_page (int, optional): Number of records per page. Defaults to 50.

    Returns:
        pd.DataFrame: A DataFrame containing works for the specified parameters.
    """
    # construct the api url with the given institution ids, publication year, publication types, publiction open access statuses, page number, and items per page
    url = (
        "https://api.openalex.org/works?"
        f"filter=corresponding_institution_ids:{'|'.join(institution_ids)},"
        f"publication_year:{publication_year},"
        f"type:{'|'.join(publication_types)},"
        f"oa_status:{'|'.join(publication_oa_statuses)}"
        f"&page={page}&per-page={items_per_page}"
    )

    # send a GET request to the api and parse the json response
    response = requests.get(url)
    json_data = response.json()

    # convert the json response to a dataframe
    df_json = pd.DataFrame.from_dict(json_data["results"])

    next_page = (
        not df_json.empty
    )  # check if the dataframe is empty (i.e., no more pages available)
    # if there are more pages, recursively fetch the next page
    if next_page:
        df_json_next_page = get_works_by_corresponding_institutions(
            institution_ids,
            publication_year,
            publication_types,
            publication_oa_statuses,
            page=page + 1,
            items_per_page=items_per_page,
        )
        df_json = pd.concat([df_json, df_json_next_page])

    return df_json


def get_works_by_ror(
    ror_id: str, publication_year: int, page: int = 1, items_per_page: int = 50
):
    """
    Fetch works from the OpenAlex API for a given ROR ID and publication year.

    Args:
        ror_id (str): The institution's ROR ID.
        publication_year (int): The publication year to filter by.
        page (int, optional): The current page number for pagination. Defaults to 1.
        items_per_page (int, optional): Number of records per page. Defaults to 50.

    Returns:
        pd.DataFrame: A DataFrame containing the retrieved works.
    """
    # construct the api url with the given ror id, publication year, publication types, page number, and items per page
    url = (
        "https://api.openalex.org/works?"
        f"filter=institutions.ror:{ror_id},"
        f"publication_year:{publication_year}"
        f"&page={page}&per-page={items_per_page}"
    )

    # send a GET request to the api and parse the json response
    response = requests.get(url)
    json_data = response.json()

    # convert the json response to a dataframe
    df_json = pd.DataFrame.from_dict(json_data["results"])

    next_page = (
        not df_json.empty
    )  # check if the dataframe is empty (i.e., no more pages available)
    # if there are more pages, recursively fetch the next page
    if next_page:
        df_json_next_page = get_works_by_ror(
            ror_id, publication_year, page=page + 1, items_per_page=items_per_page
        )
        df_json = pd.concat([df_json, df_json_next_page])

    return df_json


def get_all_outgoing_referenced_works(work_ids: List[str]):
    """
    Retrieve works cited by the given works from the OpenAlex API.

    This function takes a list of work IDs and gathers all works that each
    of those works cite from the OpenAlex API. The process is performed recursively
    to capture all pages of results.

    Args:
        work_ids (List[str]): The list of work IDs.

    Returns:
        pd.DataFrame: A DataFrame containing outgoing references for each work.
    """

    def get_outgoing_referenced_work(
        work_id: str, page: int = 1, items_per_page: int = 50
    ):
        """
        Retrieve works cited by a single work from the OpenAlex API.

        Args:
            work_id (str): The work ID.
            page (int, optional): The current page number for pagination. Defaults to 1.
            items_per_page (int, optional): Number of records per page. Defaults to 50.

        Returns:
            pd.DataFrame: A DataFrame of outgoing references for the work.
        """
        # construct the api url with the given work id, page number, and items per page
        url = (
            "https://api.openalex.org/works?"
            f"filter=cited_by:{work_id}"
            f"&page={page}&per-page={items_per_page}"
        )

        # send a GET request to the api and parse the json response
        response = requests.get(url)
        json_data = response.json()

        # convert the json response to a dataframe
        df_json = pd.DataFrame.from_dict(json_data["results"])

        next_page = (
            not df_json.empty
        )  # check if the dataframe is empty (i.e., no more pages available)
        # if there are more pages, recursively fetch the next page
        if next_page:
            df_json_next_page = get_outgoing_referenced_work(
                work_id, page=page + 1, items_per_page=items_per_page
            )
            df_json = pd.concat([df_json, df_json_next_page])

        # add the 'work_id' to the dataframe
        df_json["original_work"] = work_id
        return df_json

    df_reference = pd.concat(map(get_outgoing_referenced_work, work_ids))
    return df_reference


def get_all_incoming_referenced_works(work_ids: List[str]):
    """
    Retrieve works that cite the given works from the OpenAlex API.

    This function takes a list of work IDs and gathers all works that cite each
    of those works from the OpenAlex API. The process is performed recursively
    to capture all pages of results.

    Args:
        work_ids (List[str]): A list of work IDs to search for citations.

    Returns:
        pd.DataFrame: A DataFrame containing citing works, with a column
        'original_work' indicating the work they cite.
    """

    def get_incoming_referenced_works(
        work_id: str, page: int = 1, items_per_page: int = 50
    ):
        """
        Recursively retrieve citing works for a single work ID.

        Args:
            work_id (str): The work ID.
            page (int, optional): The current page number for pagination. Defaults to 1.
            items_per_page (int, optional): Number of records per page. Defaults to 50.

        Returns:
            pd.DataFrame: A DataFrame of citing works for the given work ID.
        """
        # construct the api url with the given work id, page number, and items per page
        url = (
            "https://api.openalex.org/works?"
            f"filter=cites:{work_id}"
            f"&page={page}&per-page={items_per_page}"
        )

        # send a GET request to the api and parse the json response
        response = requests.get(url)
        json_data = response.json()

        # convert the json response to a dataframe
        df_json = pd.DataFrame.from_dict(json_data["results"])

        next_page = (
            not df_json.empty
        )  # check if the dataframe is empty (i.e., no more pages available)
        # if there are more pages, recursively fetch the next page
        if next_page:
            df_json_next_page = get_incoming_referenced_works(
                work_id, page=page + 1, items_per_page=items_per_page
            )
            df_json = pd.concat([df_json, df_json_next_page])

        # add the 'work_id' to the dataframe
        df_json["original_work"] = work_id
        return df_json

    df_reference = pd.concat(map(get_incoming_referenced_works, work_ids))
    return df_reference
