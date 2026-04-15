Transferring data into NGC can happen in 1 of 3 ways:
1. Pip install for python packages. See the [environments guide](./guides/environments.md)
2. Git repository cloning/pulling using the Git Mirror Manager. See the [git repos guide](./guides/git_repos.md)
3. SFTP. See below.

The SFTP server acts as a link between the outside and NGC and is by default disabled for everyone. The link is bidirectional `outside <--> SFTP <--> NGC` so you can both import and export if allowed.

If you need to move something in or out of NGC and you cannot use method 1 or 2, reach out to a server admin. In your message include what you have to move and any relevant documentation stating that the transfer is legal. For moving sensitive data into NGC a data processing agreement (or similar) is required. For moving sensitive data out of NGC approval from data-specific PI is required.

Once your data move request is approved an SFTP account will be created for you or your existing account will be re-enabled and you will be given exclusive access to one of three directories in the SFTP server. Note that this means two things: 1. it's a completely separate account and 2. if none of the three directories are available your move has to wait. The directory structure inside the SFTP looks like this:
```
/data/upload
/data/upload2
/data/upload3
```

### Once you've been allocated a directory: 

Always first navigate to the *local* directory you want to either upload from or download to, and _then_ log in to the SFTP.

To log in to the SFTP *from the outside* use the following command _AFTER PUTTING IN YOUR NEW USERNAME AND REMOVING THE <>_ :
```
sftp -oHostKeyAlgorithms=+ssh-rsa -P 6433 <YOUR_SFTP_USERNAME_HERE>@sftp.spc.ngc.dk
```
To log in to the SFTP *from the inside* use the following command _AFTER PUTTING IN YOUR NEW USERNAME AND REMOVING THE <>_ :
```
sftp <YOUR_SFTP_USERNAME_HERE>@cld076-0004.cld076.vmc
```

To upload data to the SFTP go to your allocated upload directory and use `put` (assuming you logged into the SFTP from the directory where `my_great_checkpoint.ckpt` is stored):
```
cd /data/upload2
put my_great_checkpoint.ckpt
```

To download data from the SFTP go to your allocated upload directory and use `get` :
```
cd /data/upload2
get my_great_checkpoint.ckpt
```

### SFTP tips
Use the l prefix to usual commands such as pwd or cd to e.g. navigate in the local system _from the sftp_. E.g. to check files in the current _local_ directory use `lls`, or to check which _local_ directory you are currently in use `lpwd` and to nagivate elsewhere use `lcd`.
