#!/bin/sh 

#Author: Marina Schmidt
#
#This script is used to setup the bash environmnent variables for the use of mappot_fitacf 
#
export PATH=`pwd`:$PATH
#Assumes this is the default key file
export KEYFILE="rainbow.key"

if [ -f "$current_path/north_extensions" ] && [ -f "$current_path/south_extensions" ]
then 
    export MAPPOTEXTENSIONSPATH=`pwd`
else 
    echo "Please set the environment variable MAPPOTEXTENSIONSPATH to where the extensions files are located"
    echo "To set the variable use the command: export MAPPOTEXTENSIONSPATH=path/to/mappot/extensions/file"
fi

if [ -f "$current_path/rainbow.key" ]
then
    export KEYFILEPATH=`pwd`
else 
    echo "Please set the environment variable KEYFILEPATH to where the key file is located"
    echo "To set the variable use the command: export KEYFILEPATH=path/to/key/file"
    echo "If you wish to not use a keyfile then the default grey scale will be used."
fi

