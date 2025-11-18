# JupyterHub AI Lab (GPU Enabled)

Uma solução robusta de JupyterHub containerizado com suporte nativo a GPU (NVIDIA CUDA 12), projetada para colaboração em equipes de Data Science.

## 🌟 Destaques

* **Dual-Stack Kernel:** PyTorch (Base) e TensorFlow (Isolado) no mesmo ambiente.
* **GPU Ready:** Configurado para NVIDIA Drivers e CUDA 12.
* **TensorFlow GPU Fix:** Solução implementada para TF 2.x reconhecer GPU dentro do Docker.
* **Modo República:** Sistema de arquivos compartilhado com gerenciamento automático de permissões (ACL/SetGID).
* **Configuração Dinâmica:** Usuários e senhas gerenciados via arquivo `.env`.

## 📦 Stack Tecnológica

* **Imagem Base:** `ghcr.io/vcasadei/pytorch-tensorflow-cuda12-ai-ml:latest`
* **Kernels:**
    1.  **Python 3 (PyTorch GPU):** PyTorch 2.x, Pandas, Scikit-Learn.
    2.  **Python 3 (TensorFlow GPU + Keras):** TF 2.x [and-cuda], Keras, TF Hub, Graphviz.

## 🚀 Instalação (Deploy em 5 Minutos)

### 1. Clone o projeto
```bash
git clone [https://github.com/vcasadei/jupyter-ai-lab.git](https://github.com/vcasadei/jupyter-ai-lab.git)
cd jupyter-ai-lab
```


### 2. Crie o arquivo `.env`

Crie um arquivo `.env` na raiz com suas configurações:

Ini, TOML

```
HUB_PASSWORD=sua_senha_secreta
HOST_WORK_DIR=/home/seu_usuario/jupyter-ai-lab/all_work
HUB_USERS=usuario1,usuario2,usuario3
HUB_ADMINS=usuario1

```

### 3. Configure as Permissões do Host

Para o compartilhamento funcionar, execute no servidor:

Bash

```
# Cria pasta e instala ACL
mkdir -p all_work
sudo apt install acl

# Configura permissão de grupo (users) e herança
sudo chown -R 1000:100 all_work
sudo chmod g+s all_work
sudo setfacl -R -d -m g::rwx all_work
sudo setfacl -R -m g::rwx all_work

```

### 4. Execute

Bash

```
docker compose up -d

```

Acesse em `http://localhost:8080`

## 🛠️ Manutenção

-   **Adicionar Usuários:** Edite `HUB_USERS` no `.env` e rode `docker compose up -d`.
    
-   **Atualizar Imagem:** `docker compose pull` e depois `docker compose up -d`.
    

## 👤 Autor

**Vitor Casadei** ([@vcasadei](https://github.com/vcasadei))
