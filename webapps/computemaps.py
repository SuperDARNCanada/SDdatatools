from DARNprocessing import ConvectionMaps
import os

def compute_maps(date, integration_time):
    data_path = "/home/marina/data/"
    omni_path = os.getcwd() + "/omni/"
    plot_path = os.getcwd() + "/plots/"
    map_path = os.getcwd() + "/maps/"

    convec_map = ConvectionMaps(None,{'date': date,
                                      'integration_time': integration_time,
                                      'datapath': data_path,
                                      'plotpath': plot_path,
                                      'omnipath': omni_path,
                                      'mappath': map_path,
                                      'image_extension': 'png'})
    convec_map.generate_grid_files()
    convec_map.generate_map_files()
    convec_map.generate_RST_convection_maps()
    convec_map.cleanup()

if __name__ == '__main__':
    compute_maps("20160301",120)
