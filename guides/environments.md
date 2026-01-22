Set up your environment on the login node (ssh login)

### Conda 

```
module load miniconda3/4.12.0
conda config --add channels https://nexus.mgmt.cld/repository/ngc-cloud-conda/main
conda config --remove channels defaults
conda config --set ssl_verify /etc/pki/ca-trust/source/anchors/ngc-ca-cld.pem
pip install ....
```

### Pip stand-alone
```
module load anaconda3/2024.02

export VENV_PATH=MYPATH
python3.11 -m venv $VENV_PATH
$VENV_PATH/bin/pip install -U pip setuptools

$VENV_PATH/bin/pip install YOUR_PACKAGES_HERE
```
### Poetry (currently not working)

```
module load anaconda3/2024.02

export VENV_PATH=MYPATH
python3.11 -m venv $VENV_PATH

$VENV_PATH/bin/pip install -U pip setuptools
$VENV_PATH/bin/pip install poetry

$VENV_PATH/bin/poetry source add –priority=primary NGC https://vmc-nexus-01-ngc.vmc/repository/ngc-coud-pypi/simple
$VENV_PATH/bin/poetry config certificates.NGC.cert false
```
