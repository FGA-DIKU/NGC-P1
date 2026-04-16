### Always start your session with (without -Y nothing will work):
```
ssh -Y login
```

### Method 1 (preferred): Access through the scheduler
To get 4 CPUS allocated for 1 hour (adapt as needed):
```
qsub -I -X -l walltime=00:01:00:00 -l nodes=1:ppn=4
ml load R/4.0.0
ml load rstudio/1.4.1106
rstudio
```
After putting in the ```qsub``` command the scheduler will try to find resources for your job and as soon as it finds those it will redirect your current terminal session to the node with your resources. After this you continue with the next commands. 
For example if you started on the login node your terminal would go from looking like this: ```[seblla@cld076-0001 ~]$``` to this ```[seblla@worker06 ~]$```, assuming your job got scheduled on worker06. Then you continue with the ```ml load``` commands etc.

If you finish before your allocated time runs out press control+D or simply close the terminal with the job.

### Method 2: Access through Worker01
To work on worker01 (wild west no resource allocation node)
```
ssh -Y worker01
ml load R/4.0.0
ml load rstudio/1.4.1106
rstudio
```


