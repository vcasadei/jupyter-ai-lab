# Base: PyTorch com CUDA 12
FROM quay.io/jupyter/pytorch-notebook:cuda12-python-3.11

LABEL maintainer="vcasadei"
LABEL description="PyTorch + TensorFlow (GPU Support) + Multi-Kernel"

USER root

# 1. Dependências de Sistema e ACL
RUN apt-get update && apt-get install -y --no-install-recommends \
    graphviz git acl \
    && echo "umask 002" >> /etc/bash.bashrc \
    && echo "umask 002" >> /etc/profile \
    && apt-get clean && rm -rf /var/lib/apt/lists/*

# 2. Ponto de montagem
RUN mkdir -p /home/jovyan/work_shared && fix-permissions /home/jovyan/work_shared

USER ${NB_UID}

# 3. Kernel 1: PyTorch (Base)
RUN mamba install --quiet --yes \
    'scikit-learn' 'pandas' 'matplotlib' 'seaborn' 'scikit-image' \
    && mamba clean --all -f -y
RUN python -m ipykernel install --user --name python3 --display-name "Python 3 (PyTorch GPU)"

# 4. Kernel 2: TensorFlow (Isolado + GPU Fix)
RUN mamba create --quiet --yes -n tf_env python=3.11 \
    'scikit-learn' 'pandas' 'matplotlib' 'ipykernel' 'pydot' 'graphviz' \
    && mamba clean --all -f -y

# Instalação via PIP dentro do env para garantir CUDA libs do TF
RUN /opt/conda/envs/tf_env/bin/pip install --no-cache-dir \
    "tensorflow[and-cuda]" "keras" "tensorflow-datasets" "tensorflow-hub"

# Registro do Kernel
RUN mamba run -n tf_env python -m ipykernel install --user --name tf_env --display-name "Python 3 (TensorFlow GPU + Keras)"

# Fix permissão apenas na home (Rápido)
USER root
RUN fix-permissions "/home/${NB_USER}"
USER ${NB_UID}
