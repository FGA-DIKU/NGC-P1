# Resources:
- [Environments and PIP](./guides/environments.md)
- [Git repositories](./guides/git_repos.md)
- [GPU Job template](./templates/GPUJob.sh)
- [Handy links](./links.md)
- [Node overview](#node-overview)
- [Transferring data and SFTP](./guides/transfer_data.md)

# Onboarding Process
To get into the compute environment you need two accounts a "VDI account" and an "HPC account" because to access the compute environment you log into a VDI from your local computer and then from the VDI you can ssh to the compute environment i.e. `LOCAL ---> VDI ---> HPC`. 

(1) To get the VDI account you must send a *signed* user creation form to support@ngc.dk. To get the form and the signature contact Sebastian Llambias at snl@di.ku.dk. 
This process usually takes 1-2 weeks and will get you set up on NGC's Omnissa Horizon Client. Once this step is done you will be able to access a Linux and a Windows VDI.
(2) *After* (1) is done you must contact me (Sebastian) again and include your VDI username so I can set up a corresponding account for you on the HPC. You will get a temporary password which you need to change here: https://cld076-0000.cld076.vmc/ipa/ui (access this link from the browser _inside the VDI_). 
Once your password is changed you can access the HPC using `ssh login` (from the terminal _inside the VDI_) and I will give your HPC user the necessary permissions so you can access the needed data.

# Node overview:

## Login Node
Access: ```ssh login```
Usage: use to install your environment and queue jobs (see [GPU Jobs](./templates/GPUJob.sh)). DO NOT run anything heavy on this node. It is made of paper.

## Interactive Nodes:
Access: ```ssh worker01```
Usage: Debugging, faster jobs, testing. Anything goes. No rules. 

## Job Nodes:
Access: Through the [Moab-TORQUE](https://docs.adaptivecomputing.com/mwm/7-0/Content/pbsintegration.html) scheduler (see [GPU Jobs](./templates/GPUJob.sh)).
Usage: HPC workloads of up to 7 days.


# Data overview

## Fast Storage
```
/projects/users/data/
├── UCPH/
|   ├── CoBra/
|   ├── DeepFetal/
|   |   ├── ultrasound/
|   |   ├── projects/
|   ├── ICP/
|   |   ├── organized_data/
|   |   ├── projects/
|   ├── MartinSillesen/
```

## Slow Storage
```
/storage/archive
├── UCPH/
|   ├── asparagus/
|   ├── CoBra/
|   |   ├── computerome/
|   |   ├── organized_data/
|   |   ├── projects/
|   |   ├── tables/
|   |   ├── software/
|   ├── DeepFetal/
|   |   ├── ultrasound/
|   |   ├── SDS/
|   |   ├── SP/
|   ├── FOMO25/
|   ├── MartinSillesen/
|   |   ├── archived_projects/
|   |   ├── data/
|   ├── PHAIR/
|   |   ├── adr/
|   |   ├── dhr/
|   |   ├── phair_backup/
```
