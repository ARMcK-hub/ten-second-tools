# nSync
nSync is an archival script and play-on-words of rsync. 
It was written out of necessity for a linux alternative to the `RoboMirror` project located within this same repository.

nSync offers the following features:
- mirror archiving of files using rsync, ACLs not included
- file change logging with execution stats
- force overwrite of special file types like .hc
- regular job storage in form of config file


Also see `RoboMirror` for a similar PowerShell implementation.
>**Note**: nSync works from file checksums while RoboMirror uses Windows PowerShell's Robocopy - which works by filename.

</br>

# Usage
0. Clone repository and install the 1 dependency, jq. jq is utilized for proper config file parsing.
```
apt-get install -y jq
```

1. Enable execution
```
chmod +x ./nsync.sh
```

2. Rename to default and modify config file for any jobs you'd like to execute regularly.
```
mv ./config/example_config.json ./config/config.json
nano ./config/config.json
```

3. Execute script the script as given. Elevated priviledges will be required for write.
```
sudo ./nsync.sh -j myjob
```
or
```
sudo ./nsync.sh -s /path/to/source -d /path/to/destination -c /different/config/file.json
```
