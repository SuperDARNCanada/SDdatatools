from DARNprocessing import ConvectionMaps
from datetime import datetime, timedelta
import os

def compute_maps(date, integration_time,start_time):
    data_path = "/home/marina/data/"
    omni_path = os.getcwd() + "/omni/"
    plot_path = os.getcwd() + "/static/"
    map_path = os.getcwd() + "/maps/"

    # get the hour and minute with out colon for file name
    start_hour = start_time[0:2]
    start_minute = start_time[3:]

    # calculate end time
    start_date = datetime.strptime('{date} {HHMM}'.format(date=date,
                                                          HHMM=start_time),
                                   '%Y%m%d %H:%M')
    end_date = start_date + timedelta(seconds=integration_time)
    end_time = end_date.strftime('%H:%M')

    convec_map = ConvectionMaps(None,{'date': date,
                                      'integration_time': integration_time,
                                      'start_time': start_time,
                                      'end_time': end_time,
                                      'datapath': data_path,
                                      'plotpath': plot_path,
                                      'omnipath': omni_path,
                                      'mappath': map_path,
                                      'image_extension': 'png'})
    convec_map.generate_grid_files()
    convec_map.generate_map_files()
    convec_map.generate_RST_convection_maps()
    convec_map.cleanup()
    filename = 'static/{date}.{hour}{minute}.00.png'.format(date=date,
                                                     hour=start_hour,
                                                     minute=start_minute)
    print(filename)
    return filename


if __name__ == '__main__':
    compute_maps("20160301",120,"10:04")
