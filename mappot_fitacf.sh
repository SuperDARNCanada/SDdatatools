#!/bin/sh
#-----------------------------------------#
#       Author: Marina Schmidt            #
#-----------------------------------------#


#************* NOTE ******************#
# Following Bash style guide          #
#*************************************#


#---------------------------------------
#   Convection Map script
#---------------------------------------
#
#What does this script do? 
#   1. Unzips fitcon data for a given date and hemisphere
#   2. Places all data into a folder with the date and hemisphere in the folder name
#   3. Obtains omni files from the website (if needed) for the given date
#   4. Parses omni file to IMF format
#   5. Generates convections maps for the given day (post script format .ps)
#   6. Converts post script files to pdf format
#   7. Reports all errors to stderr and warnings to stdout 
#
#----------------------------------------
#   How to run
#---------------------------------------
#   1. Get off your chair and move your legs really fast (joking)
#   2. step one! Make sure rst is installed 
#   3. Make sure you have the fitcon data and extensions files 
#   4. Run: 
#           ./mappot_fitcon.sh <hemisphere (north or south)> <YYYYMMDD>
#   5. If you want it to run with verbose output:
#           ./mappot_fitcon.sh <hemisphere (north or south)> <YYYYMMDD> -vb
#
#   Example:
#       To generate convection maps for the southern hemisphere for the date 2017-11-01
#       $ ./mappot_fitcon.sh south 20171101 
#       To generate convection maps for the northern hemisphere for the date 2017-11-01
#       $ ./mappot_fitcon.sh north 20171101
#       with the verbose option
#       $ ./mappot_fitcon.sh north 20171101 -vb



#What do those exit values mean? 

#----------------------------------------
#       Exit value list
#----------------------------------------
# -1 : command error
# 0  : successful
# 1  : not enough arguements
# 2  : file not found
# 3  : empty file
# 4  : segfault
# 5  : rst function failure



#-------------------------------------------
#   Default values
#-------------------------------------------

INTEGRATIONTIME=120 # 120 seconds -> 2 minutes, standard integration time
MINIMUMRANGE=2  
FMAX=30000000
VEMAX=10000
DELAY=600 # 600 seconds -> 10 minutes this is the defualt delay time for omni sattalite information

#------------------------------------------
#   Functions to make my life easier 
#------------------------------------------




#----------------------------------------
#arguement_check:
#   simple if statement to check 
#       if there is enough arguements
# purpose: to reduce code copying 
#
# parameters: 
#       $1: number of arguements
#       $2: expected number
#       $3: Usage message
#--------------------------------------

function arguement_check(){
    
    # $# - number of arguements
    if [ $# -ne 3]
    then 
        echo "Error: $# passed in, expecting 3" >&2
        echo "Usage: arguement_check <number of arguements> <expected number> <usage message>" >&2
        exit 1;
    fi

    if [ $1 -ne $2 ]
    then
        echo "Error: $1 passed in, expecting $2" >&2
        echo "Usage: $3" >&2
        exit 1;
    fi
}



#----------------------------------------
#error_check:
#   simple if statement to check if there is an error
# purpose: to reduce code copying 
#
# parameters: 
#       $1: exit value of the function
#       $2: function name 
#       $3: error code value 
#               (please look at exit list to know what to send)
#--------------------------------------

function error_check(){
     
    # $# - number of arguements
    arguement_check $# 3 "error_check <exit value of the function> <function name> <error code value>"

    if [ $1 -ne 0 ]
    then
        echo "Error: $2 function exited with the following value: $1" >&2
        if [ $1 -eq 139 ]
        then
            echo "Error: Segfault occured" >&2
            exit 4;
        fi
        exit $3;
    fi
}

#------------------------------------------------------
#warning_check:
#   simple if statement to check if there is an error
# purpose: same reason as error_check but sometimes
#          we do not want to exit the script
#
# parameters: 
#       $1: exit value of the function
#       $2: function name 
#------------------------------------------------------

function warning_check(){
     
    # $# - number of arguements   
    arguement_check $# 2 "warning_check <exit value of the function> <function name>"

    if [ $1 -ne 0 ]
    then
        echo "Warning: $2 function exited with the following value: $1"
    fi
}


#------------------------------------------------------
#warning_file_check:
#   simple if statement to check if a file is empty
# purpose: minimizing copying 
#
# parameters: 
#       $1: file name
#------------------------------------------------------

function warning_file_check()
{
     # $# - number of arguements
     arguement_check $# 1 "warning_file_check <file name>"
   
     # -s checks if the file has a size of 0
     if [ ! -s "$1" ]
     then
         echo "Warning: $1 is empty, it will not be included in the convection map process"
         rm -f $1
         return -1;
     fi
     return 0;

}
#------------------------------------------------------
#file_check:
#   simple if statement to check if a file is empty
# purpose: minimizing copying
#   calls warning_file_check as it does the same thing
#   however, exits the code. 
#   Sometimes empty files lead to segfaults later on :/
#
# parameters: 
#       $1: file name
#------------------------------------------------------


function file_check()
{

    # $# - number of arguements
    arguement_check $# 1 "file_check <file name>"

    warning_file_check $1 > /dev/null
    # $? - return value of the previously ran command
    if [ $? -ne 0 ]
    then
        echo "Error: $1 is empty"
        exit 3;
    fi
}



#------------------------------------------------------
#warning_file_check:
#   Remove rst files
# purpose: To remove all extra generated files from 
#           the convection map process.
# Note: this code is called later in the code to allow
#       for debugging purposes just in case something
#       goes wrong. 
#
# parameters: 
#       $1: file name
#------------------------------------------------------

function cleanup()
{

    # $# - number of arguements
    arguement_check $# 1 "cleanup <file name>"


    rm -f ${1}.grd 
    rm -f ${1}.*.grid

    rm -f ${1}.hmb.map
    rm -f ${1}.*.map
    rm -f ${1}.empty.map
}


#
#TODO: Maybe move this function to its own script because users may find it useful for other projects? 
#

#
#TODO: Get solar wind information :) 
#

#------------------------------------------------------
#get_omni_file:
#   Obtains omni file from: https://omniweb.sci.gsfc.nasa.gov/form/omni_min.html
#       then formats it into IMF format
# purpose: Download and parse omni data into an IMF format 
#
# parameters: 
#       $1: date
#------------------------------------------------------

function get_omni_file()
{
 
    # $# - number of arguements
    arguement_check $# 1 "get_omni_file <date>"

    #Same trick rst uses
    #Convert to EPOCH UNIX time to save the grief on determining the past days date
    local epoch_date=`date +%s -d "$1 0000"`
    epoch_date=$((epoch_date - 600))
    
    #Omni on does the dates upto the hour so we cannot put minutes in
    #However, rst does account for extra data added to the file and will look for when the ground time and the delayed sattalite time matches up. 
    #We just need to make sure we are far enough back in the past... or else rst just substitutes 9999 in ... le sigh
    local start_date=`date -d @$epoch_date +"%Y%m%d%H"`
    

    #Timming how fast downloading a daily file takes
    if [ "$verbose" == "-vb" ]
    then
        local START=$(date +%s.%N)
    fi

     #Submit the omni variables to the website and obtain the url where the lst file is stored
   
    local omni_url=`curl -d  "activity=ftp&res=min&spacecraft=omni_min&start_date=${start_date}&end_date=${1}23&vars=13&vars=14&vars=17&vars=18&submit=Submit" https://omniweb.sci.gsfc.nasa.gov/cgi/nx1.cgi \
                        | grep -oh http.*.lst\" \
                        | grep -oh http.*.lst `
    # -z : checks if the content of a variable is zero "empty"
    if [ -z $omni_url ]
    then
        echo "Warning: No Omni file for this given date: $1 "
        return 2;
    fi

    #for some reason the url is http but to curl (download) the file you need https
    # because that is where it is actually stored... 
    #using sed to replace http with  https
    corrected_url=`sed 's\http\https\g' <<< $omni_url`
    
    #download the omni file for the given data
    #The original omni file is kept for debugging purposes :)        
    curl $corrected_url > omni_${1}_original.txt

    if [ "$verbose" == "-vb" ]
    then 
        local END=$(date +%s.%N)
        local DIFF=$(echo "$END - $START" | bc)
        echo "curl download time: $DIFF seconds"
    fi

    local omni_file=omni_${1}_original.txt

#
#TODO: Need to determine a way when all the data is bad to throw warning
#

    #doy- day of the year
    #Note: We do not throw away bad data, rst knows how to handle it... sort of
    #      Refer to IMF observations of the readme to see various outcomes. 
    while IFS=" " read -r year doy hour minute IMFmagnitude bx by bz;
    do 
        local month=`date -d "${year}0101 + ${doy} days - 1 day" +"%m"`
        local day=`date -d "${year}0101 + ${doy} days - 1 day" +"%d"`
        printf "%s %s %s %d %d 00 %f %f %f\n" $year $month $day $hour $minute $bx $by $bz >> omni_${1}.txt
    done < $omni_file

    #this obsolete right now... never a better way to determine when the data is bad.
    if [ ! -s omni_${1}.txt ]
    then
        echo "Warning: there was not good data in the Omni file"
        return 1;
    fi

    return 0;
}

#--------------------------------------------------
#           MAIN CODE
#--------------------------------------------------

main "$@"

# $# - number of arguements passed to a script or function
#I don't call my function here because of the or clause 
if [ $# -lt 2 ] || [ $# -gt 3 ]
then 
        echo "Error: $# passed in, expecting 2 or 3" >&2
        echo "Usage: ./mappot_fitcon.sh <hemisphere (north or south)> <YYYYMMDD> <verbose (-vb) optional>" >&2
        exit 1;
   
fi

hemisphere=$1
name=$2
verbose=$3

#sets pipefail to return the last most pipe command that exited
#with a non-zero return value 
set -o pipefail

if ! ls ./${name}.* 1> /dev/null 2>&1;
then
    echo "Error: There are no data files for this given date $name"
    exit 2;
fi


#Reads in the data file extensions 
if [ "$hemisphere" == "south" ]
then
    # -f : check for the existance of a file
    # !  : Negation
    if [ ! -f "south_extensions" ]
    then 
        echo "Error: south_extensions file is missing"
        echo "       You can download it off the github page: https://github.com/SuperDARNCanada/mapping"
        exit -1;
    else
        hemisphere="-sh"
        #Reads a file into an array 
        readarray data_extensions < "south_extensions"
    fi
elif [ "$hemisphere" == "north" ]
then
    if [ ! -f "north_extensions" ]
    then 
        echo "Error: north_extensions file is missing"
        echo "       You can download it off the github page: https://github.com/SuperDARNCanada/mapping"
        exit -1;
    else
        hemisphere=""
        readarray data_extensions < "north_extensions"
    fi
else
    echo "Error: $1 is not an option"
    echo "Usage: ./mappot_fitcon.sh <hemisphere (north or south)> <YYYYMMDD> <verbose (-vb) optional>" >&2
    exit -1;
fi

if [ ! -d "${name}_${1}" ]
then
    mkdir ${name}_${1}
fi

cd ${name}_${1} 
error_check $? "cd" -1 

#counter is used to determine how many grid files are created
counter=0

#@ : mean give me everything! 
for data_extension in "${data_extensions[@]}"
do
    file_name=`tr -d " " <<< ${name}.${data_extension}`
    error_check $? "tr" -1

    #if the data does not exist then check for gz file
    #extract the gz file; otherwise throw a warning that the file
    #does not exist
    if [ ! -f "../$file_name" ]
    then
           
        if [ -f "../${file_name}.gz"  ]
        then 
           gzip -d ../${file_name}.gz 2>&1; 
           error_check $? "gzip" -1;
           cp ../${file_name} .;
           error_check $? "cp" -1;
       else
           echo "Warning: ${file_name}.gz does not exist, this file will not be included in the convection map";
           continue;
        fi
                   
    else
        cp ../${file_name} .
        error_check $? "cp" -1;
    fi

    # A case where we do not want to stop if the file is empty
    warning_file_check $file_name
    if [ $? -ne 0 ]
        then
            continue;
    fi

    #use make grid to make grid files :)
    extension=`echo "$data_extension" | cut -d '.' -f2`
    error_check $pipefail "echo | cut" -1
    
    make_grid $verbose_option -new -i $record_length -minrng $min_range -fmax $f_max -vemax $vemax $file_name > ${name}.${extension}.grid
    warning_check $? "make grid" 5
    warning_file_check ${name}.${extension}.grid
    
    # $? - return value of the previously executed command
    if [ $? -eq 0 ]
    then
        counter=$((counter+1))
    fi 

done

if [ $counter -eq 0 ]
then
    echo "Error: No grid files were generated for the $1 hemisphere, please make sure there is data files for the date: $name"
    exit 2;
fi

combine_grid $verbose_option -new ${name}.*.grid > ${name}.grd
error_check $? "combine grid" 5
file_check ${name}.grd

map_grd $verbose_option $hemisphere -l 50 -new ${name}.grd > ${name}.empty.map
error_check $? "map grid" 5
file_check ${name}.empty.map


map_addhmb $verbose_option $hemisphere -new ${name}.empty.map > ${name}.hmb.map
error_check $? "map addhmb" 5
file_check ${name}.hmb.map

if [ ! -f omni_${name}.txt ]
then 
    get_omni_file $name 
    omni_returnvalue=$?
fi

if [ $omni_returnvalue -eq 0 ] && [ -s omni_${name}.txt ]
then
    
    # mapp_addimf options:
    # -d  : delay time, format hh:mm
    # -if : 
    map_addimf $verbose_option -new  -d 00:10 -if omni_${name}.txt ${name}.hmb.map > ${name}.imf.map
    error_check $? "map addimf" 5
    file_check ${name}.imf.map

    imf_extension="imf"
    imf_option="-imf"
    
else
    echo "Warning: IMF file was not generated"
    imf_extension="hmb"
    imf_option=""
fi

#map_addmodel options:
# -o : order option
# -d : 
map_addmodel $verbose_option -new -o 8 -d l ${name}.${imf_extension}.map > ${name}.model.map
error_check $? "map addmodel" 1
file_check ${name}.model.map 

map_fit $verbose_option -new ${name}.model.map > ${name}.map
error_check $? "map fit" 1
file_check ${name}.map


#
#TODO: I wonder if it is possible to get the timstamps of each integration time and then name 
#       each ps file after their times... might be nicer then some arbitrary number 
#

#map_plot options
#   -ps     : output post script convection map files
#   -mag    :
#   -rotate :
#   -logo   :
#   -modn   :
#   -fit    :
#   -grd    :
#   -ctr    :
#   -imf    : use imf data, this will only be used if we have good imf data
#   -extra  :
#   -coast  :   
#   -vecp   :
#   -vkeyp  : 
#   -time   :
#   -pot    :
#   -vkey   : vector key file, we use rainbow.key
#

#
#TODO: check for rainbow key file 
#

map_plot -new -ps -mag -rotate -logo -modn -fit -grd -ctr ${imf_option} -extra -coast -vecp -vkeyp -pot -time -vkey rainbow.key ${name}.map 2>/dev/null
error_check $? "map plot" 1



#Convert ps_files to pdfs 
for ps_file in *.ps 
do
    if [ "$verbose_option" == "-vb" ]
    then
        echo $ps_file
    fi
    timeout 20 ps2pdf $ps_file
    error_check $? "ps2pdf" -1
done

cleanup $name
