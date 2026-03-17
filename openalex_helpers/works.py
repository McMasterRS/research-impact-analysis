from typing import List

import pandas as pd
import requests
from pyalex import Works


def get_works_by_dois(dois: List[str]):
    """
    Fetch works from the OpenAlex API for the given DOIs.

    This function queries the OpenAlex API for works associated with one or
    more DOIs. If additional pages are available, it recursively fetches them
    and concatenates them into a single pandas DataFrame.

    Args:
        dois (List[str]): A list of DOIs for which to retrieve works.

    Returns:
        pd.DataFrame: A DataFrame containing the works retrieved for the specified DOIs.
    """
    json_data = Works().filter_or(doi=dois).get()
    df = pd.DataFrame(json_data)

    return df


def get_works_by_author(author_id: str):
    """
    Fetch works from the OpenAlex API for a specified author.

    Args:
        author_id (str): The ID of the author.

    Returns:
        pd.DataFrame: A DataFrame containing the works retrieved for the specified author.
    """
    json_data = Works().filter(author={"id": author_id}).get()
    df = pd.DataFrame(json_data)

    return df


def get_works_by_corresponding_institutions(
    institution_ids: List[str],
    publication_year: int,
    publication_types: List[str],
    publication_oa_statuses: List[str],
):
    """
    Fetches works from the OpenAlex API for corresponding institutions, year, publication types, and OA statuses.

    Args:
        institution_ids (List[str]): The IDs of the corresponding institution.
        publication_year (int): The publication year to filter by.
        publication_types (List[str]): Types of publications to include.
        publication_oa_statuses (List[str]): Open access statuses to include.

    Returns:
        pd.DataFrame: A DataFrame containing works for the specified parameters.
    """
    json_data = (
        Works()
            .filter_or(corresponding_institution_ids=institution_ids)
            .filter(publication_year=publication_year)
            .filter_or(type=publication_types)
            .filter_or(oa_status=publication_oa_statuses)
            .get()
    )
    df = pd.DataFrame(json_data)

    return df


def get_works_by_ror(ror_id: str, publication_year: int):
    """
    Fetch works from the OpenAlex API for a given ROR ID and publication year.

    Args:
        ror_id (str): The institution's ROR ID.
        publication_year (int): The publication year to filter by.

    Returns:
        pd.DataFrame: A DataFrame containing the retrieved works.
    """
    json_data = (
        Works()
            .filter(institutions={"ror": ror_id})
            .filter(publication_year=publication_year)
            .get()
    )
    df = pd.DataFrame(json_data)

    return df


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

    def get_outgoing_referenced_work(work_id: str):
        """
        Retrieve works cited by a single work from the OpenAlex API.

        Args:
            work_id (str): The work ID.

        Returns:
            pd.DataFrame: A DataFrame of outgoing references for the work.
        """
        json_data = Works().filter(cited_by=work_id).get()
        df = pd.DataFrame(json_data)

        return df

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

    def get_incoming_referenced_works(work_id: str):
        """
        Recursively retrieve citing works for a single work ID.

        Args:
            work_id (str): The work ID.

        Returns:
            pd.DataFrame: A DataFrame of citing works for the given work ID.
        """
        json_data = Works().filter(cites=work_id).get()
        df = pd.DataFrame(json_data)

        return df

    df_reference = pd.concat(map(get_incoming_referenced_works, work_ids))
    return df_reference
