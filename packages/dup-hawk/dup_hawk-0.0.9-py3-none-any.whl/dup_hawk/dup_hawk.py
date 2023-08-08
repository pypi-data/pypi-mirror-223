import logging as log
import os
import sys

# from .__version__ import __title__, __version__
from importlib.metadata import version
from typing import List

import click
import numpy as np
import openai
import pandas as pd
from dotenv import load_dotenv
from openai.embeddings_utils import get_embedding
from scipy.spatial.distance import cdist

from dup_hawk.github import Github

TITLE = "dup_hawk"
__version__ = version(__package__)

load_dotenv()

EMBEDDING_MODEL = "text-embedding-ada-002"
SIMILARITY_THRESHOLD_DEFAULT = 0.85

# We aren't exactly figuring out how many tokens each issue has, but instead sort of "dumb"
# Checking that their are less than 1,000 words in an issue.
PSEUDO_TOKEN_LIMIT = 1000

log.basicConfig(level=log.INFO)


@click.command()
@click.version_option(
    version=__version__,
    prog_name=TITLE,
)
@click.option(
    "--git-repo-url",
    default=None,
    required=True,
    help="GitHub repo URL that you want to mark duplicate issues for.",
)
@click.option(
    "--git-pat-token",
    default=os.getenv("GITHUB_PAT_TOKEN"),
    help="GitHub PAT token of the github user that will be marking the issues.",
)
@click.option(
    "--openai-api-key",
    default=os.getenv("OPENAI_API_KEY"),
    help="OpenAI API key for generating embeddings.",
)
@click.option(
    "--similarity-threshold",
    default=SIMILARITY_THRESHOLD_DEFAULT,
    help="The threshold for how similar issues need to be to be marked as duplicates.",
)
def dup_hawk_click(
    git_repo_url: str,
    git_pat_token: str,
    openai_api_key: str,
    similarity_threshold: float,
):
    dup_hawk(git_repo_url, git_pat_token, openai_api_key, similarity_threshold)


def dup_hawk(
    git_repo_url: str,
    git_pat_token: str,
    openai_api_key: str,
    similarity_threshold: float,
):
    openai.key = openai_api_key
    g: Github = Github(git_pat_token)
    log.info(f"Getting issues from {git_repo_url}")
    repo_issues: List[dict] = g.get_issues(git_repo_url, state="open")
    log.info(f"Found {len(repo_issues)} issues, converting to embeddings")
    df, dist_df = create_embeddings_and_dfs(repo_issues, similarity_threshold)
    log.info(f"Finding duplicates")
    duplicates_dict = mark_duplicates_from_dfs(df, dist_df)
    log.info(f"Tagging duplicates")
    for github_issue_number in duplicates_dict:
        for duplicate_number in duplicates_dict[github_issue_number]:
            log.debug(
                f"Tagging {duplicate_number} as a duplicate of {github_issue_number}"
            )
            g.tag_issue(
                github_issue_number, git_repo_url, [f"ai-dup-{duplicate_number}"]
            )
    log.info(f"Done!")


def create_embeddings_and_dfs(
    repo_issues: List[dict],
    similarity_threshold: float = SIMILARITY_THRESHOLD_DEFAULT,
) -> tuple[pd.DataFrame, pd.DataFrame]:
    """
    Reaches out to the OpenAI API to get embeddings for each issue and then creates
    a dataframe with the embeddings and a dataframe with the distances between each

    Args:
        repo_issues (List[dict]): A list of dicts from the GitHub API

    Returns:
        tuple[pd.DataFrame, pd.DataFrame]: _description_
    """
    df: pd.DataFrame = pd.DataFrame(repo_issues)
    # Combine title and body of the issue
    df["text"] = df["title"] + " " + df["body"]
    df.dropna(subset=["text"], inplace=True)

    # Create a mask for texts with token count exceeding the limit
    mask = df["text"].apply(lambda x: len(x.split()) > PSEUDO_TOKEN_LIMIT)

    # Print the "number" column for rows where the mask is True
    filtered_numbers = df[mask]["number"].tolist()
    log.info(f"Filtered out issues with too many tokens: {filtered_numbers}")
    df = df[~mask]

    # Get embeddings for each issue
    log.info("Creating embeddings, please wait...")
    df["embeddings"] = df["text"].apply(lambda x: get_embedding(x, EMBEDDING_MODEL))

    log.info("Creating distance matrix...")
    distances = cdist(list(df["embeddings"]), list(df["embeddings"]), metric="cosine")
    distances[distances > 1 - similarity_threshold] = np.nan
    dist_df = pd.DataFrame(distances)
    dist_df.index = df.index
    dist_df.columns = df.index
    return df, dist_df


def mark_duplicates_from_dfs(df: pd.DataFrame, dist_df: pd.DataFrame) -> dict:
    """
    returns a dict where the keys are the issue ids and the value is a list of duplicate IDs

    Args:
        df (pd.DataFrame): the dataframe with the issues
        dist_df (pd.DataFrame): the distance dataframe, which shows how "far away" issues are from each other

    Returns:
        dict: a dict where the keys are the issue ids and the value is a list of duplicate IDs
    """
    duplicates_dict = {}

    # Find duplicates for each issue
    for idx, row in df.iterrows():
        log.debug(f"Issue: {row['title']}")
        log.debug(f"Possible duplicates:")
        duplicates = dist_df.loc[idx].dropna().index
        duplicates_df = df.loc[duplicates]
        log.debug(duplicates_df)
        # Add id and corresponding duplicates to the dictionary
        if len(duplicates_df) > 1:
            duplicates_dict[row["number"]] = duplicates_df["number"].tolist()
            duplicates_dict[row["number"]].remove(row["number"])
        # This will only be a list of duplicates
        # else:
        #     duplicates_dict[row["number"]] = []
    return duplicates_dict


if __name__ == "__main__":
    if len(sys.argv) == 1:
        dup_hawk_click.main["--help"]
    else:
        dup_hawk_click()
