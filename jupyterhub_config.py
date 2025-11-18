import os
import docker

c = get_config()

# --- Helper Function ---
# Função para limpar a string do .env e transformar em lista
def get_user_set(env_var_name):
    users_str = os.environ.get(env_var_name, '')
    if not users_str:
        return set()
    # Divide por vírgula e remove espaços em branco acidentais
    return set(u.strip() for u in users_str.split(',') if u.strip())

# --- Autenticação ---
c.JupyterHub.authenticator_class = 'dummy'
c.DummyAuthenticator.password = os.environ.get('HUB_PASSWORD', 'senha_padrao_insegura')

# Lê do ambiente e converte para set
allowed = get_user_set('HUB_USERS')
admins = get_user_set('HUB_ADMINS')

# Garante que os admins também estejam na lista de permitidos
c.Authenticator.allowed_users = allowed.union(admins)
c.Authenticator.admin_users = admins

# --- DockerSpawner ---
c.JupyterHub.spawner_class = 'dockerspawner.DockerSpawner'
c.DockerSpawner.image = os.environ.get('DOCKER_NOTEBOOK_IMAGE', 'ghcr.io/vcasadei/pytorch-tensorflow-cuda12-ai-ml:latest')
c.DockerSpawner.network_name = 'jupyterhub-network'
c.DockerSpawner.use_internal_ip = True
c.DockerSpawner.remove = True

# --- GPU & Privilégios ---
c.DockerSpawner.extra_host_config = {
    "privileged": True,
    "device_requests": [docker.types.DeviceRequest(count=-1, capabilities=[["gpu"]])]
}

# --- Persistência e Compartilhamento ---
# Pega o caminho do host via variável de ambiente ou usa padrão
host_work_dir = os.environ.get('HOST_WORK_DIR', '/opt/jupyterhub_data/all_work')

c.DockerSpawner.volumes = {
    host_work_dir: '/home/jovyan/work_shared'
}

# --- Comandos de Inicialização (Permissões) ---
# Força umask 002 e define a pasta padrão de trabalho
c.DockerSpawner.cmd = ["/bin/sh", "-c", "umask 002 && start-singleuser.sh"]
c.DockerSpawner.notebook_dir = '/home/jovyan/work_shared'

# --- Ambiente ---
c.DockerSpawner.environment = {
    'CHOWN_HOME': 'yes',
    'CHOWN_HOME_OPTS': '-R',
    'NB_UID': 1000,
    'NB_GID': 100, # Grupo Users
}

c.JupyterHub.hub_ip = 'jupyterhub'
c.JupyterHub.hub_port = 8081
