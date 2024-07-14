import subprocess
import logging
from .setup_ssh_key import create_ssh_path

logging.basicConfig(level=logging.INFO)
log = logging.getLogger("__Airflow GitHub Synchronization__")

def clone_public_repo(git_url, git_branch):
    username = git_url.split('/')[-2]
    repo_split = git_url.split('/')
    
    if ".git" not in git_url:
        repo = repo_split[-1]
    else:
        repo = repo_split[-1].split('.')[0]
    
    clone_cmd = f"git clone -b {git_branch} https://github.com/{username}/{repo}.git"

    try:
        log.info(f'Cloning the target Git Repo {git_url} ==============>')
        subprocess.run(clone_cmd, shell=True, check=True)
        log.info(f'{git_url} cloned successfully')
    except subprocess.CalledProcessError as e:
        log.info(f'Git clone failed with error: {e}')

    return repo


def clone_private_repo(git_url, git_branch, git_token, ssh_private_key):
    username = git_url.split('/')[-2]
    repo_split = git_url.split('/')
    
    if "https" in git_url:
        
        if ".git" not in git_url:
            repo = repo_split[-1]
        else:
            repo = repo_split[-1].split('.')[0]
        
        clone_cmd = f"git clone -b {git_branch} https://{git_token}@github.com/{username}/{repo}.git"

        try:
            log.info(f'Cloning the target Git Repo {git_url} ==============>')
            subprocess.run(clone_cmd, shell=True, check=True)
            log.info(f'{git_url} cloned successfully')
        except subprocess.CalledProcessError as e:
            log.info(f'Git clone failed with error: {e}')

    if "git@github.com" in git_url:
    
        if ".git" not in git_url:
            repo = repo_split[-1]
            clone_cmd = f"git clone -b {git_branch} {git_url}.git"
        else:
            repo = repo_split[-1].split('.')[0]
            clone_cmd = f"git clone -b {git_branch} {git_url}"

        private_key_file = create_ssh_path(ssh_private_key)

        git_ssh_command = f'GIT_SSH_COMMAND="ssh -i {private_key_file} -o IdentitiesOnly=yes"'

        command = f'{git_ssh_command} {clone_cmd}'

        try:
            log.info(f'Cloning the target Git Repo {git_url} ==============>')
            subprocess.run(command, shell=True, check=True)
            log.info(f'{git_url} cloned successfully')
        except subprocess.CalledProcessError as e:
            log.info(f'Git clone failed with error: {e}')

    return repo