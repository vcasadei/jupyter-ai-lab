# JupyterHub AI Lab (GPU Enabled)

A robust, containerized JupyterHub solution with native NVIDIA GPU support (CUDA 12), designed for Data Science teams and research.

This project offers two modes of operation:
1.  **Multi-User Hub:** Full JupyterHub setup with shared storage and user management.
2.  **Standalone Lab:** Run a single JupyterLab instance for personal use.

## 🌟 Highlights

* **Dual-Stack Kernel:** PyTorch (Base) and TensorFlow (Isolated) in the same environment.
* **GPU Ready:** Pre-configured for NVIDIA Drivers, CUDA 12, and cuDNN.
* **TensorFlow GPU Fix:** Custom installation to ensure TF 2.x recognizes GPU inside Docker.
* **"Republic" Mode (Hub Only):** Shared file system with automatic permission management (ACL/SetGID), allowing real-time collaboration on files.
* **Dynamic Config:** Users and passwords managed via `.env` file.

## 📦 Tech Stack

* **Base Image:** `ghcr.io/vcasadei/pytorch-tensorflow-cuda12-ai-ml:latest`
* **Kernels:**
    1.  **Python 3 (PyTorch GPU):** PyTorch 2.x, Pandas, Scikit-Learn, Seaborn.
    2.  **Python 3 (TensorFlow GPU + Keras):** TF 2.x [and-cuda], Keras, TF Hub, Graphviz.

---

## 🚀 Mode 1: JupyterHub (Multi-User)

Ideal for teams. Includes authentication, persistent user storage, and a shared "commons" folder.

### 1. Clone the repository
```bash
git clone [https://github.com/vcasadei/jupyter-ai-lab.git](https://github.com/vcasadei/jupyter-ai-lab.git)
cd jupyter-ai-lab
```

### 2. Configure Environment

Create a `.env` file in the root directory:

Ini, TOML

```
HUB_PASSWORD=your_secure_password
HOST_WORK_DIR=/home/your_user/jupyter-ai-lab/all_work
HUB_USERS=user1,user2,user3
HUB_ADMINS=user1

```

### 3. Setup Host Permissions (Crucial)

For the shared folder collaboration to work, you must configure ACLs on the host directory:

Bash

```
# Create folder and install ACL
mkdir -p all_work
sudo apt install acl

# Configure group ownership (users) and inheritance
sudo chown -R 1000:100 all_work
sudo chmod g+s all_work
sudo setfacl -R -d -m g::rwx all_work
sudo setfacl -R -m g::rwx all_work

```

### 4. Launch

Bash

```
docker compose up -d

```

Access at `http://localhost:8080`.

----------

## 🏎️ Mode 2: Standalone JupyterLab (Single User)

Ideal for individual research or quick testing. No Hub, no database, just pure JupyterLab.

### Quick Start

Run the following command to launch a disposable instance with GPU support:

Bash

```
docker run -it --rm \
    --gpus all \
    -p 8888:8888 \
    -v "${PWD}":/home/jovyan/work \
    ghcr.io/vcasadei/pytorch-tensorflow-cuda12-ai-ml:latest

```

### Access

-   Open your browser at `http://localhost:8088`.
    
-   Look at the terminal output to copy the **token** (e.g., `http://127.0.0.1:8888/lab?token=...`).
    

### Persistence

In the command above, the `-v "${PWD}":/home/jovyan/work` flag mounts your current folder into the container. Any file you save in JupyterLab will be saved in your current terminal directory.

----------

## 🛠️ Maintenance (Hub Mode)

-   **Add Users:** Edit `HUB_USERS` in `.env` and run `docker compose up -d`.
    
-   **Update Image:** Run `docker compose pull` followed by `docker compose up -d`.
    
-   **Logs:** Check logs with `docker compose logs -f jupyterhub`.
    

## 👤 Author

**Vitor Casadei**

-   GitHub: [@vcasadei](https://github.com/vcasadei)
