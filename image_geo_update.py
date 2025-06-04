"""
    program to update the geo coordinates in an .jpg image file
"""
import sys
import os
from argparse import ArgumentParser
from aipy.img_extensions import get_file_list, get_geo_from_gpx, get_img_timestamp, \
                                set_geo2exif, print_exif_data

if sys.platform.startswith('linux'):
    DIR='/home/aimholt/projects/TestData/pictures_tracklogs'
elif sys.platform.startswith('win'):
    DIR='C:\\Users\\Andreas\\projects\\TestData\\pictures_tracklogs'

parser=ArgumentParser(
    prog='image_geo_update',
    description='backend-tool to update image geo data from tracking tools')
group1=parser.add_mutually_exclusive_group(required=True)
group1.add_argument('-i', '--image',
            help='select only image with filename',
            type=str)
group1.add_argument('-a', '--all',
            help='select all images in working directory',
            action='store_true')
parser.add_argument('-e', '--exif',
            help='print current exif data',
            action='store_true')
parser.add_argument('-s', '--save',
            help='save changes to images',
            action='store_true', default=False)
parser.add_argument('-d', '--directory',
            help='select working directory, current is: '+DIR,
            type=str)
args=parser.parse_args()

TZONE='Europe/Berlin'

### making image filelist
img_file_list=[]
if args.all:
    img_file_list=get_file_list(dir=DIR,m_pattern='^.*\\.(jpg)$')
if args.image:
    img_file_list.append(os.path.join(DIR,args.image))

### making gpx file list
gpx_file_list=get_file_list(dir=DIR,m_pattern='^.*\\.(gpx)$')

### making list of geo coordinates from multiple gpx files sorted by time 
coord_list=[]
for file in gpx_file_list:
    for item in get_geo_from_gpx(file):
        coord_list.append(item)        
coord_list.sort(key=lambda x: x['dt'], reverse=False)
print(f'number of geo entries found: {len(coord_list)} - oldest: {coord_list[0]['dt']} - newest: {coord_list[len(coord_list)-1]['dt']}')

### for each file open and read the timestamp
count=0
for file in img_file_list:
    if args.exif:
        print("\n>>>>>>>>>>>>>>>>>>>>>>>>> EXIF data of image: "+args.image)
        print_exif_data(os.path.join(DIR,file))

    found=False
    coord_dt_before=None
    coord_dt_after=None
    img_dt=     get_img_timestamp(file)
    img_name=   file.lstrip(DIR)
    max_time_diff=60

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
        ### set coords to image file
        if args.save:
            set_geo2exif(coord, file)
        found=False
    elif not found:
        if  coord_dt_before != None:
            time_diff_before = (img_dt - coord_dt_before).seconds
        if  coord_dt_after != None:
            time_diff_after = (coord_dt_after - img_dt).seconds
        if  (time_diff_before < max_time_diff or time_diff_after  < max_time_diff)  and \
            time_diff_before <= time_diff_after:
            if args.save:
                set_geo2exif(coord, file)
            print(
                f'{img_name:<20s} IMG({img_dt.date()} {img_dt.time()}) - '
                f'COORD({coord_dt_before.date()} {coord_dt_before.time()}; LAT: {coord['lat']:9.6f}; LON: {coord['lon']:9.6f}; -{time_diff_before}s)'
                )
        elif(time_diff_before < max_time_diff or time_diff_after  < max_time_diff)  and \
            time_diff_before > time_diff_after:
            if args.save:
                set_geo2exif(coord, file)
            print(
                f'{img_name:<20s} IMG({img_dt.date()} {img_dt.time()}) - '
                f'COORD({coord_dt_after.date()} {coord_dt_after.time()}; LAT: {coord['lat']:9.6f}; LON: {coord['lon']:9.6f}; +{time_diff_after}s)'
            )
if args.save:
    print('>> changes saved to images')
else:
    print('>> nothing saved to images(only with option "-s")')
exit()