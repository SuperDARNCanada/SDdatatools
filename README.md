SuperDARN data tools 
=====================

This python package provides modules that wrap around RST functions for users that wish to use python for scripting and for webapplication backends. 

The following RST methods that are implemented: 
* grid file generation
* map file generation
* convection plots generation using RST (future developement will include pydarn as a possible option)
* OMNI file download for IMF data

You can import the package by: 

    import DARNprocessing

For quick and easy use for generation of convection maps and plots, one can also use the installed built in scripts:
    
    fitacf2convectionMap.py --help 

## Dependencies 
The following packages need to be installed before being able to use the following scripts
* RST 4.1 and higher - https://github.com/SuperDARN/rst
* python 2.7 or newer

## Fitted data restrictions 
Please be aware this library currently only works with fitacf (2.5 and 3.0), or lmfit2 data types. Fit files must be converted to either fitacf or lmfit2. 

Future developement will include wrappers for this as well. 

## Installation 
Running the following command to install the python package:
    
    sudo python setup.py install 

## Example code 
Using the module to generate convection plots:
    
    from DARNprocessing import ConvectionMaps
    data_path = os.getcwd() + "/data/"
    omni_path = os.getcwd() + "/omni/"
    plot_path = os.getcwd() + "/plots/"
    map_path = os.getcwd() + "/maps/"

    convec_map = ConvectionMaps(None,{'date': "20060301",
                                      'datapath': data_path,
                                      'plotpath': plot_path,
                                      'omnipath': omni_path,
                                      'mappath': map_path})
    convec_map.generate_grid_files()
    convec_map.generate_map_files()
    convec_map.generate_RST_convection_maps()
    convec_map.cleanup()

Using an installed script:
    
    fitacf2convectionMap.py --image-extension png --datapath /data/fitcon/2016/01/ -p /home/schmidt/2016/01/north/ 20160101


## Developement 

