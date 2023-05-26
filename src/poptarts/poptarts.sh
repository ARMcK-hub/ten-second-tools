#!/bin/bash

# constants
blue='\e[0;34m'
red='\e[0;31m'
nocolor='\e[0m'

#####  POptArts  #####
# terminal help function, exits script after execution
helpFunction()
{
   echo -e "${blue}"
   echo "Usage: $0 -flavor cherry -frozen false"
   echo -e "\t -flavor   Flavor of POptArts. Type: string."
   echo -e "\t -frozen   Flag for frozen PoptArts. Type: boolean"
   echo -e "${nocolor}"
   exit 1
}

# acquiring opts, prints helpFunction in case parameter is non-existent
while getopts "flavor:frozen:" opt
do
   case "$opt" in
      flavor ) flavor="$OPTARG" ;;
      frozen ) isFrozen="$OPTARG" ;;
      ? ) helpFunction ;;
   esac
done

# Print helpFunction in case parameters are empty
if [ -z "$flavor" ] || [ -z "$isFrozen" ]
then
   echo -e "\t${red}Some or all of the parameters are empty${nocolor}";
   helpFunction
fi


#####  SCRIPT  #####
# TODO
