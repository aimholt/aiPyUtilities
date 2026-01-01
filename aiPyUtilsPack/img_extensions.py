"""
    module for image processing extensions
"""
import os
import gpxpy
import piexif
import re
from zoneinfo import ZoneInfo
from datetime import datetime
from fractions import Fraction

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

def print_exif_data(path):
    """
        print all exif data of a image file
    """    
    exif_dict = piexif.load(path)
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
    fnames.sort()
    path_list = []
    for fname in fnames:
        path=os.path.join(dir,fname)
        if os.path.isfile(path) and p.match(fname):
            path_list.append(path)
    return path_list

def deg_to_dms(coord_dec, type):
    """ 
    this function converts decimal coordinates into the DMS (degrees, minutes and seconds) format.
    It also determines the cardinal direction of the coordinates.
    """
    if      coord_dec > 0 and type=='lat':
        direction = 'N'
    elif    coord_dec < 0 and type=='lat':
        direction = 'S'
    elif    coord_dec > 0 and type=='lon':
        direction = 'E'
    elif    coord_dec < 0 and type=='lon':
        direction = 'W'
    else:
        direction = "-"

    deg = int(abs(coord_dec))
    decimal_minutes = (abs(coord_dec) - deg) * 60
    min = int(decimal_minutes)
    sec = Fraction((decimal_minutes - min) * 60).limit_denominator(100)

    #deg, coord_dec = divmod(coord_dec * 60, 60)
    #min, sec = divmod(coord_dec * 60, 60)
    ##return int(deg), int(min), float(sec), direction
    return deg, min, sec, direction

def dms_to_exif(dms_degrees, dms_minutes, dms_seconds):
    """
    This function converts DMS (degrees, minutes and seconds) to values that can
    be used with the EXIF (Exchangeable Image File Format).

    :param dms_degrees: int value for degrees
    :param dms_minutes: int value for minutes
    :param dms_seconds: fractions.Fraction value for seconds
    :return: EXIF values for the provided DMS values
    :rtype: nested tuple
    """
    exif_format = (
        (dms_degrees, 1),
        (dms_minutes, 1),
        (int(dms_seconds.limit_denominator(100).numerator), int(dms_seconds.limit_denominator(100).denominator))
    )
    return exif_format

def set_geo2exif(coord, img_path):
    """
    This function adds GPS values to an image using the EXIF format.
    This fumction calls the functions deg_to_dms and dms_to_exif_format.

    :param image_path: image to add the GPS data to
    :param latitude: the north–south position coordinate
    :param longitude: the east–west position coordinate
    """    
    ### convert coords from dec to dms
    lat_dms=deg_to_dms(coord['lat'],type='lat')
    lon_dms=deg_to_dms(coord['lon'],type='lon')
    ### convert dms from to exif format
    lat_exif = dms_to_exif(lat_dms[0], lat_dms[1], lat_dms[2])
    lon_exif = dms_to_exif(lon_dms[0], lon_dms[1], lon_dms[2])

    gps_coords = {
        piexif.GPSIFD.GPSVersionID: (2, 0, 0, 0),
        piexif.GPSIFD.GPSLatitude: lat_exif,
        piexif.GPSIFD.GPSLatitudeRef: lat_dms[3],
        piexif.GPSIFD.GPSLongitude: lon_exif,
        piexif.GPSIFD.GPSLongitudeRef: lon_dms[3]
        }
    exif_dict = piexif.load(img_path)
    exif_dict['GPS'] = gps_coords
    exif_bytes = piexif.dump(exif_dict)
    piexif.insert(exif_bytes, img_path)
    return