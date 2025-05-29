"""
    program to update the geo coordinates in an .jpg image file
"""
from aipy.img_extensions import get_file_list, get_geo_from_gpx, get_img_timestamp, print_exif_data

import sys

if sys.platform.startswith('linux'):
    DIR='/home/aimholt/projects/TestData/pictures_tracklogs'
elif sys.platform.startswith('win'):
    DIR='C:\\Users\\Andreas\\projects\\TestData\\pictures_tracklogs'

TZONE='Europe/Berlin'

### making list of files in working directory
img_file_list=get_file_list(dir=DIR,m_pattern='^.*\\.(jpg)$')
gpx_file_list=get_file_list(dir=DIR,m_pattern='^.*\\.(gpx)$')

### making list of geo coordinates from multiple gpx files sorted by time 
coord_list=[]
for file in gpx_file_list:
    for item in get_geo_from_gpx(file):
        coord_list.append(item)        
coord_list.sort(key=lambda x: x['dt'], reverse=False)
print(f'number of geo entries: {len(coord_list)} - oldest: {coord_list[0]['dt']} - newest: {coord_list[len(coord_list)-1]['dt']}')
### for each file open and read the timestamp
count=0
for file in img_file_list:
    found=False
    coord_dt_before=None
    coord_dt_after=None
    img_dt=     get_img_timestamp(file)
    img_name=   file.lstrip(DIR)
    max_time_diff=30

    ### for each image find the best time matches in geo coordinates
    time_diff_before=max_time_diff
    time_diff_after=max_time_diff
    count+=1
    for coord in coord_list:
        if      coord['dt'] < img_dt:
            coord_dt_before=coord['dt']
        elif    coord['dt'] == img_dt:
            found=True
            break
        elif    coord['dt'] > img_dt:
            coord_dt_after=coord['dt']
            break

    ### handling of time matches and no time matches
    if found:
        print(
            f'{img_name:<20s} IMG({img_dt.date()} {img_dt.time()}) - ' 
            f'COORD({coord['dt'].date()} {coord['dt'].time()}; LAT: {coord['lat']:9.6f}; LON: {coord['lon']:9.6f};  0s)'
            )
        found=False
    elif not found:
        if  coord_dt_before != None:
            time_diff_before = (img_dt - coord_dt_before).seconds
        if  coord_dt_after != None:
            time_diff_after = (coord_dt_after - img_dt).seconds
        if  (time_diff_before < max_time_diff or time_diff_after  < max_time_diff)  and \
            time_diff_before <= time_diff_after:
            print(
                f'{img_name:<20s} IMG({img_dt.date()} {img_dt.time()}) - '
                f'COORD({coord_dt_before.date()} {coord_dt_before.time()}; LAT: {coord['lat']:9.6f}; LON: {coord['lon']:9.6f}; -{time_diff_before}s)'
                )
        elif(time_diff_before < max_time_diff or time_diff_after  < max_time_diff)  and \
            time_diff_before > time_diff_after:
            print(
                f'{img_name:<20s} IMG({img_dt.date()} {img_dt.time()}) - '
                f'COORD({coord_dt_after.date()} {coord_dt_after.time()}; LAT: {coord['lat']:9.6f}; LON: {coord['lon']:9.6f}; +{time_diff_after}s)'
            )
exit()