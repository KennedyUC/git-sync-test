import shutil
import logging

logging.basicConfig(level=logging.INFO)
log = logging.getLogger("__Airflow GitHub Synchronization__")

def copy_airflow_dag(git_repo, dags_folder):
    destination_path = '/opt/airflow/dag'
    
    if dags_folder == "root":
        try:
            shutil.copytree(git_repo, destination_path, dirs_exist_ok=True)
            log.info(f'Dags folder copied to {destination_path}')
        except Exception as exception:
            log.info(exception)
    else:
        try:
            shutil.copytree(f'{git_repo}/{dags_folder}', destination_path, dirs_exist_ok=True)
            log.info(f'Dags folder copied to {destination_path}')
        except Exception as exception:
            log.info(exception)

    shutil.rmtree(git_repo)
    log.info(f'{git_repo} removed for cleanup purposes')