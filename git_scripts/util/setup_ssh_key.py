import os
import logging

logging.basicConfig(level=logging.INFO)
log = logging.getLogger("__Airflow GitHub Synchronization__")

def create_ssh_path(ssh_private_key):
    private_key_path = os.path.expanduser('~/.ssh/git')
    private_key_file = os.path.join(private_key_path, 'id_rsa')

    os.makedirs(private_key_path, exist_ok=True)

    ssh_private_key = ssh_private_key.strip()

    ssh_private_key = '\n'.join(line.lstrip() for line in ssh_private_key.splitlines())

    ssh_private_key += '\n'

    if os.path.exists(private_key_file):
        os.chmod(private_key_file, 0o700)

    log.info(f'Writing the ssh private key to {private_key_file} =============>')
    with open(private_key_file, 'w') as key_file:
        key_file.write(ssh_private_key)

    os.chmod(private_key_file, 0o400)
    
    return private_key_file