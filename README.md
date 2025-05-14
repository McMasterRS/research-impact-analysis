# research-impact-analysis

This project contains code to query data from [OpenAlex APIs](https://docs.openalex.org/). The OpenAlex dataset describes scholarly entities and how those entities are connected to each other. Types of entities include works, authors, sources, institutions, topics, publishers, and funders.  

## Usage

The notebooks can be run on either [Google Colab](https://colab.research.google.com/) or [Jupyter Notebook](https://jupyter.org/install).  

## OpenAlex API Limitation

### Querying Works by Author Using Author Entity API

While OpenAlex's Author entity API allows direct access to publication/citation count by years, the numbers does not match with the metrics shown in the web interface. The aggregation algorithm has issues causing the numbers from the API significantly larger than true values or the numbers shown in the web interface. This is confirmed by [Jack Young](https://orcid.org/0000-0003-4626-0409) and developers from OpenAlex.  

It was then suggested by the developers to use the Work entity API and query all the publications by the author. Each publication has citation count by years and then the counts are aggregrated in the script. Using the Work entity API helps getting publication/citation numbers closer to the true values. However, upon further inspection to query results from the Work entity API, the API returns publications that do not belong to the author (even when using the Author's OpenAlex ID or ORCID in the query). It is suspected that these extra publications are published by authors with same/similar names.  
