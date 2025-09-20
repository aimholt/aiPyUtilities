import urllib3
import xml.etree.ElementTree as ET
import hashlib
import subprocess
import requests
import json
import pandas as pd
import os
import sys

ROUTER_URL =    "http://xyzrouter.internal"
USER =          "aimholt"  # Anmeldename z. B. fritz1234
PASSWORD =      "Imh2And-01"  # Anmeldekennwort
NOT_VALID_SID = "0000000000000000" # immer ungueltig
DATA_DIR =  "/home/aimholt/projects/TestData"
if sys.platform != 'linux': 
    DATA_DIR =  "C:\\Users\\Andreas\\projects\\TestData"

def get_fb_sid(fritzbox, fritz_user, fritz_pw):
    fb_sid=NOT_VALID_SID
    if fb_sid == "0000000000000000":
        session = requests.Session()
        http = urllib3.PoolManager()
        data = http.request("get", fritzbox + "/login_sid.lua").data
        tree = ET.fromstring(data)
        fb_sid = tree.findtext("SID")
        if fb_sid == "0000000000000000":
            challenge = tree.findtext("Challenge")
            hash_me = (challenge + "-" + fritz_pw).encode("UTF-16LE")
            hashed = hashlib.md5(hash_me).hexdigest()
            response = challenge + "-" + hashed
            ret = session.get(fritzbox + "/login_sid.lua", params={
                "username": fritz_user,
                "response": response
            }, verify=False, timeout=5)
            tree = ET.fromstring(ret.text)
            fb_sid = tree.findtext("SID")
            if fb_sid == "0000000000000000":
                print("fb_get_sid: Fehler beim Abrufen der SID")
                exit()
    return fb_sid

def get_struct(x, level=0, struct=[]):
    """
        get structure of a python object created by json.load
    """
    if level == 0:
        struct.append("structure of object:")
    if type(x) == dict:
        indent="="*(level+1)+str(level)
        struct.append(f'{indent}: dict with {len(x)} entries; keys:')
        for key, value in x.items():
            indent=">"*(level+1)+str(level)
            struct.append(f'{indent}: {key}  - value type {type(value)}')
            if type(value) == dict or type(value) == list:
                #struct.append(f'xxxx')
                level+=1
                get_struct(value, level=level,struct=struct)
                level-=1
    if type(x) == list:
        indent="="*(level+1)+str(level)
        if len(x)>0:
            struct.append(f'{indent}: list with {len(x)} entries; each of type {type(x[0])}')
            level+=1
            get_struct(x[0], level=level, struct=struct)
            level-=1
    return struct

def get_log_from_fb(fb_sid=None, file=None):
    """
        getting logfile from frtzbox / store it in file 
    """
    url=ROUTER_URL+'/data.lua'
    path=DATA_DIR+os.sep+file
    payload={
        'sid':          fb_sid,
        'lang':         'de',
        'page':         'log',
        'no_siderenew': '',
        }
    resp=requests.post(url,data=payload)
    if resp.status_code == 200 or resp.status_code == 200:
        log=resp.text
        with open(path, 'w') as f:
            f.write(log)
    return

def get_log_from_file(file):
    """ 
        reading json data from file 
    """
    path=DATA_DIR+os.sep+file
    with open(path, 'r') as f:
        s_var=f.read()
    return s_var

def main():
    ### get log from fritzbox
    #sid = get_fb_sid(ROUTER_URL, USER, PASSWORD)
    #log=get_log_from_fb(fb_sid=sid)
    #get_log_from_fb(fb_sid=sid, file='fritz_log.json')
    ### get log from file
    log=get_log_from_file('fritz_log.json')
    p_object=json.loads(log)
    for item in get_struct(p_object):
        print(item)

    ### formating log entries
    #for i in get_struct(x):
    #    print(i)
    #log=[]
    #for key1 in x.keys():
    #    if key1=='data':
    #        for key2 in x[key1].keys():
    #            if key2 == 'log':
    #                for x in x[key1][key2]:
    #                    log.append(f'{x['date']} {x['time']} {x['group']:>4} {x['msg']}')



if __name__ == '__main__':
    main()