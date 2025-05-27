"""
    program to update the geo coordinates in an .jpg image file
"""
from aipy.img_extensions import get_file_list, get_geo_from_gpx, get_img_timestamp

PATH='C:\\Users\\Andreas\\projects\\TestData\\pictures&tracklog'
TZONE='Europe/Berlin'

### making list of files in working directory
img_file_list=get_file_list(path=PATH,pattern='^.*\\.(jpg)$')
gpx_file_list=get_file_list(path=PATH,pattern='^.*\\.(gpx)$')

### making list of geo coordinates from multiple gpx files 
coord_list=[]
for file in gpx_file_list:
    for item in get_geo_from_gpx(file):
        coord_list.append(item)

### for each file open and read the timestamp
count=0
for file in img_file_list:
    found=False
    coord_dt_before=None
    coord_dt_after=None
    img_dt=     get_img_timestamp(file)
    img_name=   file.lstrip(PATH)

    ### for each image find the best time matches in geo coordinates
    count+=1
    for coord in coord_list:
        if      coord['time'] < img_dt:
            coord_dt_before=coord['time']
        elif    coord['time'] == img_dt:
            found=True
            break
        elif    coord['time'] > img_dt:
            coord_dt_after=coord['time']
            break

        ### handling of time matches and no time matches
    time_diff_before=None
    time_diff_after=None
    if found:
        print(
            f'{count:>2}. {img_name} ({img_dt}) - ' 
            f'exact:  COORD({coord['time'].time()}; LAT: {coord['lat']}; LON: {coord['lon']})'
            )
        found=False
    elif not found:
        if coord_dt_before != None:
            time_diff_before = (img_dt - coord_dt_before).seconds
        if coord_dt_after != None:
            time_diff_after = (coord_dt_after - img_dt).seconds
        print(
            f'{count:>2}. {img_name} ({img_dt.date()} {img_dt.time()}) -' 
            f' vor: {coord_dt_before} (-{time_diff_before}s) /'
            f' nach: {coord_dt_after} (+{time_diff_after}s)'
            )
exit()