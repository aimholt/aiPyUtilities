"""
    module for image processing extensions
"""

import os
import gpxpy
import piexif
from zoneinfo import ZoneInfo
from datetime import datetime
import re

TZONE='Europe/Berlin'

def get_geo_from_gpx(fname):
    """
        get all geo coordinates in a gpx file
    """
    gpx = gpxpy.parse(open(fname, 'r'))
    gpx_by_date=[]
    for trk in gpx.tracks:
        for trkseg in trk.segments:
            for trkpt in trkseg.points:
                gpx_by_date.append({
                    'dt':   trkpt.time.astimezone(tz=ZoneInfo(TZONE)),
                    'lat':  trkpt.latitude,
                    'lon':  trkpt.longitude
                    })
    return gpx_by_date

def print_exif_data(fname, dir):
    """
        print all exif data of a image file
    """    
    exif_dict = piexif.load(os.path.join(dir,fname))
    for ifd_name in exif_dict:
        if ifd_name != 'thumbnail':
            print(f'IFD-name: <{ifd_name}> IFD-elements: <{len(exif_dict[ifd_name])}>')
            if len(exif_dict[ifd_name])<50:
                for key in exif_dict[ifd_name]:
                    try:
                        print(f' > {key}, {exif_dict[ifd_name][key][:20]}')
                    except:
                        print(f' >>{key}, {exif_dict[ifd_name][key]}')
            else:
                print(' >> to long for dumping the elements')
    return

def get_img_timestamp(fname):
    """
        returns a datetime object of jpg timestamp
    """
    exif_dict = piexif.load(fname)
    x_datetime=str(exif_dict['Exif'][36867])
    x_datetime=x_datetime.rstrip("'")
    x_datetime=x_datetime.lstrip("b'")
    x_datetime=datetime.strptime(x_datetime,'%Y:%m:%d %H:%M:%S')
    x_datetime=x_datetime.astimezone(tz=ZoneInfo(TZONE))
    return x_datetime

def get_file_list(dir, m_pattern=''):
    """
        returns a list of filenames filtered by patterns in the defined directory
    """
    p=re.compile(m_pattern,re.IGNORECASE)
    fnames=os.listdir(dir)
    path_list = []
    for fname in fnames:
        path=os.path.join(dir,fname)
        if os.path.isfile(path) and p.match(fname):
            path_list.append(path)
    return path_list