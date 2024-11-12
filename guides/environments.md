### Conda

```
conda config --add channels https://vmc-nexus-01.ngc.vmc/repository/ngc-cloud-conda/main
conda config --remove channels defaults
```

### Poetry

```
export VENV_PATH=MYPATH
python3 -m venv $VENV_PATH

$VENV_PATH/bin/pip install -U pip setuptools
$VENV_PATH/bin/pip install poetry

$VENV_PATH/bin/poetry source add –priority=primary NGC https://vmc-nexus-01-ngc.vmc/repository/ngc-coud-pypi/simple
$VENV_PATH/bin/poetry config certificates.NGC.cert false
```
