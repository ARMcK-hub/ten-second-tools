#!/bin/bash

# defaults
configFile="./config/config.json"
overwriteTypes="*.hc"

# constants
blue='\e[0;34m'
red='\e[0;31m'
nocolor='\e[0m'

#####  POptArts  #####
# terminal help function, exits script after execution
helpFunction()
{
   echo -e "${blue}"
   echo "Usage Examples:"
   echo -e "\t$0 -s /path/to/source -d /path/to/destination -c /path/to/config.json"
   echo -e "\t$0 -j myjob"
   echo -e "\t$0 -j 'myjob myotherjob' -c ./myconfig.json"
   echo ""
   echo "Parameters:"
   echo -e "\t -s	Source path."
   echo -e "\t -d	Destination path; Example: "
   echo -e "\t -j	Space delimited list of job names, defined in config.json; Example: 'job1 job2'"
   echo -e "\t -c	Path of config file. Default: ./config/config.json; Example: '/absolute/path/config.json'"
   echo -e "${nocolor}"
   exit 1
}

# acquiring opts, prints helpFunction in case parameter is non-existent
while getopts "s:d:j:c:" opt
do
   case "$opt" in
      s ) source="$OPTARG" ;;
      d ) destination="$OPTARG" ;;
      j ) job="$OPTARG" ;;
      c ) configFile="$OPTARG" ;;
      ? ) helpFunction ;;
   esac
done

# Print helpFunction in case parameters are empty
if (([ -z "$source" ] || [ -z "$destination" ]) && [ -z "$job" ]) || (([ ! -z "$source" ] || [ ! -z "$destination" ]) && [ ! -z "$job" ])
then
   echo -e "\t${red}Some or all of the parameters are empty or configured incorrectly${nocolor}";
   helpFunction
fi


#####  nSync  #####

config=$(jq . $configFile)
jobs=$(echo $config | jq .jobs)

# returns job as JSON from config
getJob () {
		jobName=$1
		job=$(echo $jobs | jq --arg jobName "$jobName" '.[] | select(.name | contains($jobName))')
		echo $job
}

runRsyncJob () {
	source=$1
	destination=$2
	
}

# setting source and destination if job
if [ ! -z "$job" ]
then
	jobConfig=$(getJob $job)
	source=$(echo $jobConfig | jq -r .source)
	destination=$(echo $jobConfig | jq -r .destination)
fi

echo -e "\n\t${blue}Running Request: $job \tSource: $source \tDestination:$destination${nocolor}"

# performing deletes on overwriteTypes missed by rsync
echo -e "\n\tFinding Overwritable Files ($overwriteTypes) ...."
owFiles=$(find "${destination}/$(basename $source)" -type f -name $overwriteTypes)
echo -e "\tDeleted: \n$owFiles"
rm -f $owFiles

# performing rsync job
echo -e "\n\tRunning Sync...."
logFile="$destination/logs/nsync_$(basename $source).log"
sudo rsync $source $destination -mach --super --force --progress --stats --log-file $logFile

echo -e "\n\tLog written to: $logFile"
echo -e "\n\t\tYour files are now ${blue}nSync${nocolor}."
