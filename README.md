# Resources:
- [Environments and PIP](./guides/environments.md)
- [Git repositories](./guides/git_repos.md)
- [GPU Job template](./templates/GPUJob.sh)
- [Handy links](./links.md)
- [Node overview](#node-overview)
- [Transferring data and SFTP](./guides/transfer_data.md)

# Node overview:

## Login Node
Access: ```ssh login```
Usage: use to install your environment and queue jobs (see [GPU Jobs](./templates/GPUJob.sh)). DO NOT run anything heavy on this node. It is made of paper.

## Interactive Nodes:
Access: ```ssh worker01``` or ```ssh worker02```
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
