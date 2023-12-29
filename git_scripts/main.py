import click
import logging
from util.copy_dags import *
from util.setup_git_clone import *
import os
import time

logging.basicConfig(level=logging.INFO)
log = logging.getLogger("__Airflow GitHub Synchronization__")

@click.command()
@click.option("--git_branch", type=str, help="Target Git Branch for synchronization", default='main')
@click.option("--git_url", type=str, help="Github Remote url")
@click.option("--private_repo", type=bool, help="Is repo private or public", default=False)
@click.option("--git_token", type=str, help="Token for Git Authentication", default=None)
@click.option("--ssh_private_key", type=str, help="SSH private Key for Authentication to Github", default=None)
@click.option("--dags_folder", type=str, help="Target folder with the Airflow DAGs", default='root')
def main(git_branch, git_url, private_repo, git_token, dags_folder, ssh_private_key):
    git_branch      = os.getenv("GIT_TARGET_BRANCH", git_branch)
    git_url         = os.getenv("GIT_REPO_URL", git_url)
    private_repo    = os.getenv("IS_PRIVATE_REPO", private_repo)
    git_token       = os.getenv("GIT_SYNC_TOKEN", git_token)
    ssh_private_key = os.getenv("SSH_PRIVATE_KEY", ssh_private_key)
    dags_folder     = os.getenv("DAGS_TARGET_FOLDER", dags_folder)

    if not private_repo:
        git_repo = clone_public_repo(git_url, git_branch)
    else:
        git_repo = clone_private_repo(git_url, git_branch, git_token, ssh_private_key)

    copy_airflow_dag(git_repo, dags_folder)

    while True:
        time.sleep(5)

if __name__ == '__main__':
    main()