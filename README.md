# mapping 
Is a bash script that processes SuperDARN fitcon data into a convection map.


## Requirements 
To run this scritpt you will need:

* [RST] (https://github.com/SuperDARN/rst)

## Instal Notes
Instructions on how to get the script working:

1. Clone the github repository:
        ```
            git clone https://github.com/SuperDARNCanada/mapping.git
        ```
2. Then run: 
        
        source install.sh
        

* If you don't want to run this command each time you reopen a terminal then place these line in your **.bashrc**
            
                export PATH=<path to mappot_fitacf file>/:$PATH
                export KEYFILE="rainbow.key"
                export KEYFILEPATH=<path to the key file>
                export MAPPOTEXTENSIONPATH=<path to the north_extensions and south_extensions files>
**Make sure** you file in the paths correctly.


## What to Expect

The script does the following: 

1. Reads in fitcon data for the associated radars for the given hemisphere
2. Stores the files in the path <plot path>/fitcon date/hemisphere/current date/

## How To Run

After the isntallation, you can run the script from any folder. 
Change to the directory where the fitcon data is, if you do not have write permissions there then inidicate the path where the fitcon is with the option *-fitacfpath*.

To run: 
        
        mappot_fitacf --date YYYYMMDD --hemi north
        
To obtain information on the script:
           
           mappot_fitacf --help 
    
           Usage:
              mappot_file [OPTIION] [OPTION INPUT]...
            example: mappot_file -hemi south -date 20130601
            Options:
              -H | --hemi <south or north>            Hemisphere you are looking at (required)
              -d | --date YYYYMMDD                    The date you are interested in (required)
              -n | --numproc <# of processors>        The number of processors the script should use
              -s | --st HH:MM                         start time for the mappotential plots (optional)
              -e | --et HH:MM                         end time for the mappotential plots (optional)
              -f | --fitacfpath <absolute path>       path to the fitacf data (optional)
              -m | --mappath <absolute path>          path to where the covection maps will be stored based on hemisphere/year/month/day (optional)
              -o | --ominpath <absolute path>         path to where the omini will be saved to (optional)
              -p | --plotpath <absolute path>         path to where the plots will be saved. Note: the omni files will also be saved in this location (optional)
              -i | --imageextension <extension type>  the image extension you would like the plot files to be converted to. Default is pdf. (optional)
              -V | --version <rst version>            The assumed default version is 4.1 if using anything later than 4.1 please indicated it. (optional)
              -v | --vb                               verbose (optional)
              -D | --degbug                           sets the debuggin option for the script and stores all information in the logfile
              -h | --help                             help menu on the various options
            NOTE: if the start time and/or the end time is not provided then it will generate the mappotential plots for the whole day.
        

### Examples:

            mappot_fitacf --date 20171005 --hemi north -i "jpeg" -f "/data/fitcon/2017/10" 
    

