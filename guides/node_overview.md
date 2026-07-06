
# Node overview:

## Login Node
Access: ```ssh login```
Usage: use to install your environment and queue jobs (see [GPU Jobs](./templates/GPUJob.sh)). DO NOT run anything heavy on this node. It is made of paper.

## Interactive Node:
We have 1 interactive node with SSH access.

Access: ```ssh worker01```
Usage: Debugging, faster jobs, testing. Anything goes. No rules. 

## Interactive Jobs:
Interactive Jobs are regular jobs that go through the queue to the compute nodes WITH shell access.
CPU Access: ```qsub -I -l nodes=1:ppn=5 -l walltime=00:15:00```
GPU Access: ```qsub -I -l nodes=1:gpus=1:ppn=5 -l walltime=00:15:00```

Exit: ctrl+d

## Compute Nodes:
We have 6 compute nodes only accessible through the scheduler. Each node has 2 H100 GPUs with 80GB VRAM, ~750GB RAM and 64 CPU Cores.

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
|   ├── FOMO26/
|   ├── ICP/
|   |   ├── organized_data/
|   |   ├── projects/
|   ├── MartinSillesen/
|   |   ├── EHR/
|   |   ├── projects/
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
|   |   ├── genetics/
|   |   ├── SDS/
|   |   ├── SP/
|   |   ├── ultrasound/
|   ├── FOMO25/
|   ├── MartinSillesen/
|   |   ├── archived_projects/
|   |   ├── data/methylation
|   ├── PHAIR/
|   |   ├── adr/
|   |   ├── dhr/
|   |   ├── phair_backup/
```
