# research-impact-analysis

This project contains code to query data from [OpenAlex APIs](https://docs.openalex.org/). The OpenAlex dataset describes scholarly entities and how those entities are connected to each other. Types of entities include works, authors, sources, institutions, topics, publishers, and funders.  

## Usage

The notebooks can be run on either [Google Colab](https://colab.research.google.com/) or [Jupyter Notebook](https://jupyter.org/install). An instruction to run the notebooks on Syzygy, a JupyterHub service provided by Digital Research Alliance of Canada, is provided in the [`docs/syzygy.md`](docs/syzygy.md).  

## Setup

1. Clone the repository or download the ZIP file of the repository
2. Navigate to the directory where you cloned or extracted the repository
3. (Optional) Create a virtual environment and activate it to manage dependencies:
    ```bash
    python -m venv .venv
    source .venv/bin/activate
    ```
4. Install the required Python packages by running the following command in your terminal or command prompt:
    ```bash
    pip install -r requirements.txt
    ```
5. Duplicate the sample `.env.example` file and rename it to `.env`
6. Populate the `.env` file with your actual API keys
7. (Optional) Duplicate sample CSV files in the `data/` folder and populate them with the relevant information

## OpenAlex API Limitation

### Querying Works by Author Using Author Entity API

While OpenAlex's Author entity API allows direct access to publication/citation count by years, the numbers do not match with the metrics shown in the web interface. The aggregation algorithm has issues, causing the numbers from the API to be significantly larger than the true values or the numbers shown in the web interface. This is confirmed by [Jack Young](https://orcid.org/0000-0003-4626-0409) and developers from OpenAlex.  

It was then suggested by the developers to use the Work entity API and query all the publications by the author. Each publication has a citation count by years and then the counts are aggregated in the script. Using the Work entity API helps get publication/citation numbers closer to the true values. However, upon further inspection of query results from the Work entity API, the API returns publications that do not belong to the author (even when using the Author's OpenAlex ID or ORCID in the query). It is suspected that these extra publications are published by authors with the same/similar names.  
