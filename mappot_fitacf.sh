#!/bin/sh
record_length=120
min_range=2
f_max=30000000
name=$2
vemax=10000
#----------------------------------------
#       Exit value list
#----------------------------------------
# 0  : successful
# -1 : command error
# 1  : file not found
# 2  : empty file

#error_check: 
# parameters: 
#       $1: exit value 
#       $2: function name 
#       $3: error code value (please look at exit list to know what to send)
function error_check(){
    
    if [ $1 -ne 0 ]
    then
        echo "Error: $2 function exited with the following value: $1"
        exit $3;
    fi
}

function warning_check(){
    
    if [ $1 -ne 0 ]
    then
        echo "Warning: $2 function exited with the following value: $1"
    fi
}


function cleanup()
{

    rm -f ${1}.grd 
    rm -f ${1}.*.grid

    rm -f ${1}.hmb.map
    rm -f ${1}.*.map
    rm -f ${1}.empty.map
}

function file_check()
{
    warning_file_check $1 > /dev/null
    if [ $? -ne 0 ]
    then
        echo "Error: $1 is empty"
        exit 2;
    fi
}

function warning_file_check()
{

        if [ ! -s "$1" ]
        then
            echo "Warning: $1 is empty, it will not be included convection map process"
            rm -f $1
            return -1;
        fi
        return 0;
}

#get_omni_file: 
#   parameters: 
#       $1: name that the user passes into the script 
#   post: obtains the omni file from the NASA website given the default parameters for the given day
#   
#
function get_omni_file()
{


    delay=600 # 600 seconds is 10 minutes 
    
    #same trick rst uses
    #they may not write the best code but they are smart on how they do things
    #By converting to EPOCH UNIX time we just need to subtract the delay and then convert it back
    #to get the correct delayed time and day for the sattalite data. 
    #These lines save the headache of keeping track of the year, months and leap years. 
    epoch_date=`date +%s -d "$1 0000"`
    epoch_date=$((epoch_date - 600))
    
    #Omni on does the dates upto the hour so we cannot put minutes in
    #However, rst does account for extra data added to the file and will look for when the ground time and the delayed sattalite time matches up. 
    #We just need to make sure we are far enough back in the past... or else rst just substitutes 9999 in ... le sigh
    start_date=`date -d @$epoch_date +"%Y%m%d%H"`
    
    #Submit the omni variables to the website and obtain the url where the lst file is stored
    START=$(date +%s.%N)
    omni_url=`curl -d  "activity=ftp&res=min&spacecraft=omni_min&start_date=${start_date}&end_date=${1}23&vars=13&vars=14&vars=17&vars=18&submit=Submit" https://omniweb.sci.gsfc.nasa.gov/cgi/nx1.cgi  | grep -oh http.*.lst\" | grep -oh http.*.lst ` 
    
    if [ -z $omni_url ]
    then
        echo "Warning: No Omni file for this given date: $1 "
        return 2;
    fi
    #for some reason the url is http but to curl it you need https because that is where it is actually stored... 
    #using sed to replace http with  https
    corrected_url=`sed 's\http\https\g' <<< $omni_url`
    
    #download the omni file for the given data
    #I keep the original for debugging and file storage :)
    curl $corrected_url > omni_${1}_original.txt
    END=$(date +%s.%N)
    DIFF=$(echo "$END - $START" | bc)
    echo "curl download time: $DIFF seconds"
    omni_file=omni_${1}_original.txt

    #doy- day of the year
    while IFS=" " read -r year doy hour minute IMFmagnitude bx by bz;
    do 
        if [ $(echo "$bx > 900.0" | bc) -ne 0 ]
        then
            continue;
        fi
        month=`date -d "${year}0101 + ${doy} days - 1 day" +"%m"`
        day=`date -d "${year}0101 + ${doy} days - 1 day" +"%d"`
        printf "%s %s %s %d %d 00 %f %f %f\n" $year $month $day $hour $minute $bx $by $bz >> omni_${1}.txt
    done < $omni_file

    if [ ! -s omni_${1}.txt ]
    then
        echo "Warning: there was not good data in the Omni file"
        return 1;
    fi

    return 0;
}


if ! ls ./${name}.* 1> /dev/null 2>&1;
then
    echo "Error: There are no data files for this given date $name"
    exit 2
fi


#Reads in the data file extensions 
if [ "$1" == "south" ]
then
    if [ ! -f "south_extensions" ]
    then 
        echo "Error: south_extensions file is missing"
        exit -1;
    else
        hemisphere="-sh"
        readarray data_extensions < "south_extensions"
    fi
elif [ "$1" == "north" ]
then
    if [ ! -f "north_extensions" ]
    then 
        echo "Error: north_extensions file is missing"
        exit -1;
    else
        hemisphere=""
        readarray data_extensions < "north_extensions"
    fi
else
    echo "Error: $1 is not an option"
    echo "usage: ./mappot_fitacf <south or north> <YYYYMMDD> <-vb for verbose option>"
    exit -1;
fi

if [ ! -d "${name}_${1}" ]
    then
        mkdir ${name}_${1}
    fi

cd ${name}_${1} 

verbose_option=$3
counter=0
for data_extension in "${data_extensions[@]}"
do
    file_name=`tr -d " " <<< ${name}.${data_extension}`
    #if the data does not exist then check for gz file
    #extract the gz file; otherwise throw an error that the file
    #does not exist 
    if [ ! -f "../$file_name" ]
    then
           
        if [ -f "../${file_name}.gz"  ]
        then 
           gzip -d ../${file_name}.gz 2>&1; 
           error_check $? "gzip" -1;
           cp ../${file_name} .;
        else
           echo "Warning: ${file_name}.gz does not exist, this file will not be included in the convection map";
           continue;
        fi
                   
    else
        cp ../${file_name} .
    fi

    warning_file_check $file_name
    if [ $? -ne 0 ]
        then
            continue;
    fi

    #use make grid to make grid files :)
    extension=`echo "$data_extension" | cut -d '.' -f2` 
    
    make_grid $verbose_option -new -i $record_length -minrng $min_range -fmax $f_max -vemax $vemax $file_name > ${name}.${extension}.grid
    warning_check $? "make grid" 1
    warning_file_check ${name}.${extension}.grid

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
error_check $? "combine grid" 1
file_check ${name}.grd

map_grd $verbose_option $hemisphere -l 50 -new ${name}.grd > ${name}.empty.map
error_check $? "map grid" 1
file_check ${name}.empty.map


map_addhmb $verbose_option $hemisphere -new ${name}.empty.map > ${name}.hmb.map
error_check $? "map addhmb" 1

if [ ! -f omni_${name}.txt ]
then 
    get_omni_file $name 
    omni_returnvalue=$?
fi

if [ $? -eq 0 ] && [ -s omni_${name}.txt ]
then
    # Note: delay time is in the format of hr:mm if you put in 10 then it will convert it to 10 hours :/ 
    map_addimf $verbose_option -new  -d 00:10 -if omni_${name}.txt ${name}.hmb.map > ${name}.imf.map
    error_check $? "map addimf" 1
    file_check ${name}.imf.map
    imf_extension="imf"
    imf_option="-imf"
    
else
    echo "Warning: IMF file was not generated"
    imf_extension="hmb"
    imf_option=""
fi


map_addmodel $verbose_option -new -o 8 -d l ${name}.${imf_extension}.map > ${name}.model.map
error_check $? "map addmodel" 1
file_check ${name}.model.map 

map_fit $verbose_option -new ${name}.model.map > ${name}.map
error_check $? "map fit" 1
file_check ${name}.map


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
    error_check $? "ps2pdf" $error_message 1
done

cleanup $name
