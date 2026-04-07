Set up your environment on the login node (ssh login)

### Conda 

```
module load miniconda3/4.12.0
conda config --add channels https://nexus.mgmt.cld/repository/ngc-cloud-conda/main
conda config --remove channels defaults
conda config --set ssl_verify /etc/pki/ca-trust/source/anchors/ngc-ca-cld.pem
conda create -n YOUR_ENV python=PYTHON_VERSION_HERE
conda activate YOUR_ENV
pip install <YOUR_PACKAGE_HERE>
```

### Pip stand-alone
```
module load anaconda3/2024.02

export VENV_PATH=MYPATH
python3.11 -m venv $VENV_PATH
$VENV_PATH/bin/pip install -U pip setuptools

$VENV_PATH/bin/pip install YOUR_PACKAGES_HERE
```
