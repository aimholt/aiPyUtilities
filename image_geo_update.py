"""
    problem: my camera has no gps so no location information is stored in the images
    this program updates the geo coordinates in a .jpg image, when a geo tracking file is given
    - working directory is given as argument
    - inside working directory image files and one or more gpx files are expected
    - it's not expected that the time stamp in an image file is exactly found in an gpx file
    - a max-time-diff is defined to set a threshold for the time difference between image timestamp and gpx timestamp
    - the coordinates of found gpx entries are written to the exif data of the image file  
"""
from importlib.resources import path
from pathlib import Path
import sys
import os
from argparse import ArgumentParser
from aiPyUtilsPack.img_extensions import get_file_list, get_geo_from_gpx, get_img_timestamp, \
    set_geo2exif, print_exif_data

TZONE='Europe/Berlin'

def main(max_time_diff=60):
    parser=ArgumentParser(
        prog='image_geo_update',
        description='backend-tool to update image geo data with gps data from tracking tool')
    group1=parser.add_mutually_exclusive_group(required=True)
    group1.add_argument('-f', '--fname',
                help='select a single image specified (filename)',
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
    parser.add_argument('-d', '--directory', required=True,
                help='set working directory',
                type=str)
    args=parser.parse_args()

    working_dir=args.directory    

    ### >>>>> check if directory exists and is readable and writable)
    path=Path(working_dir)
    if not path.exists():
        sys.exit(f' Error: {path} does not exist')
    elif not path.is_dir():
        sys.exit(f' Error: {path} is not a directory')
    
    if args.all:
        img_fpath_list=get_file_list(dir=working_dir,m_pattern='^.*\\.(jpg)$')
    elif args.fname:
        img_fpath_list.append(os.path.join(working_dir,args.fname))
    
    ### making gpx and image fpath list
    gpx_fpath_list=get_file_list(dir=working_dir,m_pattern='^.*\\.(gpx)$')

    if len(gpx_fpath_list) == 0:
        sys.exit(f' Error: no gpx file found in {working_dir}')
    elif len(img_fpath_list) == 0:
        sys.exit(f' Error: no image file found in {working_dir}')

    geo_coord_list=[]

    print(  f'working directory: {working_dir}')
    print(  f'number of gpx files in working directory: {len(gpx_fpath_list)}')
    print(  f'number of img files in working directory: {len(img_fpath_list)}')
    
    for gpx_fpath in gpx_fpath_list:
        for geo_coordinate_item in get_geo_from_gpx(gpx_fpath):
            geo_coord_list.append(geo_coordinate_item)        
    geo_coord_list.sort(key=lambda x: x['dt'], reverse=False)
    print(  f'number of geo entries found: {len(geo_coord_list)} - '
            f'oldest: {geo_coord_list[0]['dt']} - '
            f'newest: {geo_coord_list[len(geo_coord_list)-1]['dt']}')

    ### for each fpath open and read the timestamp
    count=0
    for img_fpath in img_fpath_list:
        img_dt=get_img_timestamp(img_fpath)
        img_fname=img_fpath.lstrip(working_dir)
        found=False
        coord_dt_before=None
        coord_dt_after=None
        if args.exif:
            print("\n>>>>>>>>>>>>>>>>>>>>>>>>> EXIF data of image: "+img_fname)
            print_exif_data(os.path.join(working_dir,img_fpath))

        ### for each image find the best time matches in geo coordinates
        time_diff_before=max_time_diff
        time_diff_after=max_time_diff
        count+=1
        for coord in geo_coord_list:
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
                f'{img_fname:<20s} IMG({img_dt.date()} {img_dt.time()}) - ' 
                f'COORD({coord['dt'].date()} {coord['dt'].time()}; LAT: {coord['lat']:9.6f}; LON: {coord['lon']:9.6f};  0s)'
                )
            ### set coords to image fpath
            if args.save:
                set_geo2exif(coord, img_fpath)
            found=False
        elif not found:
            if  coord_dt_before != None:
                time_diff_before = (img_dt - coord_dt_before).seconds
            if  coord_dt_after != None:
                time_diff_after = (coord_dt_after - img_dt).seconds
            if  (time_diff_before < max_time_diff or time_diff_after  < max_time_diff)  and \
                time_diff_before <= time_diff_after:
                if args.save:
                    set_geo2exif(coord, img_fpath)
                print(
                    f'{img_fname:<20s} IMG({img_dt.date()} {img_dt.time()}) - '
                    f'COORD({coord_dt_before.date()} {coord_dt_before.time()}; LAT: {coord['lat']:9.6f}; LON: {coord['lon']:9.6f}; -{time_diff_before}s)'
                    )
            elif(time_diff_before < max_time_diff or time_diff_after  < max_time_diff)  and \
                time_diff_before > time_diff_after:
                if args.save:
                    set_geo2exif(coord, img_fpath)
                print(
                    f'{img_fname:<20s} IMG({img_dt.date()} {img_dt.time()}) - '
                    f'COORD({coord_dt_after.date()} {coord_dt_after.time()}; LAT: {coord['lat']:9.6f}; LON: {coord['lon']:9.6f}; +{time_diff_after}s)'
                )
    if args.save:
        print('>> changes saved to images')
    else:
        print('>> nothing saved to images(only with option "-s")')
    return

if __name__ == '__main__':
    main()
exit()