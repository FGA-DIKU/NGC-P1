# Jupyter noteboook

### Step 1
ssh to cluster, and install jupyter notebook. 
```
export VENV_PATH=MYPATH
python3.11 -m venv $VENV_PATH
source $VENV_PATH/bin/activate
pip install -U pip setuptools
pip install notebook jupyter
```

### Step 2
Run a Jupyter Notebook server (HPC side)
```
jupyter notebook --no-browser --port=8888
```

This will have an output like this
```
To access the notebook, open a browser at:
    http://localhost:8888/?token=abc123...
```

### Step 3
Open another terminal on the local compute and ssh to HPC. 
```
ssh -L 8888:localhost:8888 yourusername@login.HPC.cluster
```

### Step 4
Open local browser and type in
```
http://localhost:8888
```

Enter token when asked. 