# Resources:
- [Environments and PIP](./guides/environments.md)
- [Git repositories](./guides/git_repos.md)
- [GPU Job template](./templates/GPUJob.sh)
- [Handy links](./links.md)
- [Server overview](./guides/server_overview.md)
- [Transferring data and SFTP](./guides/transfer_data.md)
- [MPI](./guides/MPI-on-CLD076.docx)

# Onboarding Process
To get into the compute environment you need two accounts a "VDI account" and an "HPC account" because to access the compute environment you log into a VDI from your local computer and then from the VDI you can ssh to the compute environment i.e. `LOCAL ---> VDI ---> HPC`. 

(1) To get the VDI account you must send a *signed* user creation form to support@ngc.dk. To get the form and the signature contact Sebastian Llambias at snl@di.ku.dk. 
This process usually takes 1-2 weeks and will get you set up on NGC's Omnissa Horizon Client. Once this step is done you will be able to access a Linux and a Windows VDI.

(2) *After* (1) is done you must contact me (Sebastian) again and include your VDI username so I can set up a corresponding account for you on the HPC. You will get a temporary password which you need to change here: https://cld076-0000.cld076.vmc/ipa/ui (access this link from the browser _inside the VDI_). Once your password is changed you can access the HPC using `ssh login` (from the terminal _inside the VDI_) and I will give your HPC user the necessary permissions so you can access the needed data.

# Getting started on the HPC

For an overview of where data is stored see the [Data overview](./guides/server_overview.md#Data-overview).
For an overview of the available compute resources see the [Node overview](./guides/server_overview.md#Node-overview).

1. Set up environment: [Environments and PIP](./guides/environments.md)
2. Set up GIT repos: [Git repositories](./guides/git_repos.md)
3. Set up the file explorer: [File Explorer](./guides/file_explorer.md)
4. Test code on Worker01: [Node overview](./guides/server_overview.md#Node-overview).
5. Write job script: [GPU Job template](./templates/GPUJob.sh)
6. Start job using `qsub MYJOBSCRIPT.sh`
7. Monitor job progress and see the general queue using `showq`. Use `qstat -f JOBID` or `tracejob JOBID` for additional details

# FAQ:

### Graphical interfaces and notebooks

To use R or other applications requiring graphical interfaces see the [graphical applications](./guides/graphical_applications.md) guide.
To use Jupyter notebooks see the [jupyter notebook](./jupyter_notebook.md) guide.

### Passwords

Remember that you have up to 3 passwords for NGC: (1) Your VDI password for Omnissa, (2) Your HPC password for the compute environment, and (3) Your SFTP password. They are all independent and will be reset at different intervals, so treat them as completely separate.

To reset your HPC password go to the [IPA URL](./links.md)
To reset your SFTP password go to the [SFTP URL](.links.md)

# Advanced

### MPI 

See the [MPI Guide](./guides/MPI-on-CLD076.docx) but beware that it is complex to run jobs across multiple nodes.
