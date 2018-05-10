SuperDARN map file and plot generation scripts
===============================================

This python package provides modules that wrap around  RST functions for generating:
* grid files
* map files 
* convection plots 
and a module to download OMNI data to be included in the map file generation. 
You can import the package by: 

    import DARNprocessing

For quick and easy use for generation of convection maps and plots, one can also use the installed built in scripts:
    
    fitacf2convectionMap.py --help 

## Dependencies 
The following packages need to be installed before being able to use the following scripts
* RST - https://github.com/SuperDARN/rst
* python 2.7 or newer

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

