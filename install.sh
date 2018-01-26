#!/bin/sh 

#Author: Marina Schmidt
#
#This script is used to setup the bash environmnent variables for the use of mappot_fitacf 
#
mkdir ~/bin 
cp ./src/mappot_fitacf ./bin/mappot_fitacf

export PATH=`pwd`/bin/:$PATH >>> .bashrc 
#Assumes this is the default key file
export KEYFILE="rainbow.key" >>> .bashrc 

if [ -f "./north_extensions" ] && [ -f "./south_extensions" ]
then 
    export MAPPOTEXTENSIONSPATH=`pwd`/file_extensions >>> .bashrc  
else 
    echo "Please set the environment variable MAPPOTEXTENSIONSPATH to where the extensions files are located"
    echo "To set the variable use the command: export MAPPOTEXTENSIONSPATH=path/to/mappot/extensions/file"
fi

