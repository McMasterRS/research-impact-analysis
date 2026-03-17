import re
from typing import List

import numpy as np
import pandas as pd
import requests
from pyalex import Institutions, Publishers


def get_publisher_display_name_lookup_table(publisher_ids: List[str], num_chunk: int = 5) -> pd.DataFrame:
    def get_source_host_organization_publisher_display_name(publisher_ids):
        def get_source_host_organization_publisher_display_name_by_chunk(publisher_ids_chunk):
            json_data = Publishers().filter_or(ids={"openalex": publisher_ids_chunk}).get()
            df = pd.DataFrame(json_data)

            return df[["id", "display_name"]]
        
        # check if the length of 'publisher_ids' is less than 1
        if len(publisher_ids) < 1:
            # if true, return an empty dataframe
            return pd.DataFrame()

        # split the publisher ids into chunks and apply the function to each chunk
        chunks = np.array_split(publisher_ids, np.ceil(len(publisher_ids) / num_chunk))
        df_chunks = pd.DataFrame({"chunk": chunks})
        return pd.concat(df_chunks["chunk"].apply(get_source_host_organization_publisher_display_name_by_chunk).tolist())

    def get_source_host_organization_institution_display_name(institution_ids):
        def get_source_host_organization_institution_display_name_by_chunk(institution_ids_chunk):
            json_data = Institutions().filter_or(id=publisher_ids_chunk).get()
            df = pd.DataFrame(json_data)

            return df[["id", "display_name"]]

        # check if the length of 'institution_ids' is less than 1
        if len(institution_ids) < 1:
            # if true, return an empty dataframe
            return pd.DataFrame()

        # split the institution ids into chunks and apply the function to each chunk
        chunks = np.array_split(institution_ids, np.ceil(len(institution_ids) / num_chunk))
        df_chunks = pd.DataFrame({"chunk": chunks})
        return pd.concat(df_chunks["chunk"].apply(get_source_host_organization_institution_display_name_by_chunk).tolist())

     # filter the publisher ids to get only publisher urls
    publishers = list(filter(lambda s: re.search(r"https:\/\/openalex\.org\/P", s), publisher_ids))
    # filter the institution ids to get only institution urls
    institutions = list(filter(lambda s: re.search(r"https:\/\/openalex\.org\/I", s), publisher_ids))

    # create a dataframe with a default entry for unknown source
    df_lookup = pd.DataFrame.from_dict({"id": ["unknown source"], "display_name": ["unknown source"]})
    # concatenate the dataframes with publisher and institution display names
    df_lookup = pd.concat([df_lookup, get_source_host_organization_publisher_display_name(publishers), get_source_host_organization_institution_display_name(institutions)], ignore_index=True)
    return df_lookup
