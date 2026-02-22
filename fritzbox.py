import urllib3
import xml.etree.ElementTree as ET
import hashlib
import requests
import json
import os, sys
import re

ROUTER_URL =    "http://xyzrouter.internal"
USER =          "aimholt"  # Anmeldename z. B. fritz1234
PASSWORD =      "Imh2And-01"  # Anmeldekennwort
NOT_VALID_SID = "0000000000000000" # immer ungueltig
DATA_DIR =      "/home/andreas/projects/testData"
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
        if fb_sid == NOT_VALID_SID:
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
            if fb_sid == NOT_VALID_SID:
                print("get_fb_sid: Fehler beim Abrufen der SID")
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

def get_log_from_fb(fb_sid=None, filename=None):
    """
        delivers fritzbox logfile in json format / store it in file 
    """
    url=ROUTER_URL+'/data.lua'
    if filename:
        path=DATA_DIR+os.sep+filename
    
    payload={
        'sid':          fb_sid,
        'lang':         'de',
        'page':         'log',
        'no_siderenew': '',
        }
    resp=requests.post(url,data=payload)
    if resp.status_code == 200 or resp.status_code == 200:
        body_py=resp.json()
        if filename:
            with open(path, 'w') as file:
                json.dump(body_py, file, separators=(',', ': '), indent=2)
            file.close()
            msg=f'json logfile stored in file "{filename}"'
        else:
            msg=json.dumps(body_py, separators=(',', ': '), indent=2)

    return msg

def get_log_from_file(file):
    """ 
        reading json data from file 
    """
    path=DATA_DIR+os.sep+file
    with open(path, 'r') as f:
        s_var=f.read()
    return s_var

def main():
    opt='s'     # r: get log(json-format) from fb to sdtout or file if given
                # a: analyse log structure
                # s: search log with either native string or regEx,
                # e: experimental

    if      opt == 'r':
        sid = get_fb_sid(ROUTER_URL, USER, PASSWORD)
        msg=get_log_from_fb(fb_sid=sid, filename='fritz_log.json')
        print(msg)
    elif    opt == 'a':
        log=get_log_from_file('fritz_log.json')
        p_object=json.loads(log)
        for item in get_struct(p_object):
            print(item)
    elif    opt == 's':
        log_json=get_log_from_file('fritz_log.json')
        log_py=json.loads(log_json)
        re_search=True
        pattern_input="^..\.09\.25 12"
        if re_search:
            try:
                pattern=re.compile(pattern_input)
            except:
                print(f'error in regEx; performing normal string-search for "{pattern_input}"')
                pattern=re.compile(re.escape(pattern_input))
        else:
            pattern=re.escape(pattern_input)
        for item in log_py['data']['log']:
            log_entry=f'{item['date']} {item['time']} {item['group']:>4} {item['msg']}'
            if      re_search == True:      # re input
                if re.search(pattern, log_entry):
                    print(f'{log_entry}')
            elif    re_search == False:     # not re input
                if re.search(pattern, log_entry, re.IGNORECASE):
                    print(f'{log_entry}')
    elif    opt == 'e':        
        log=get_log_from_file('fritz_log.json')
        print(log)
if __name__ == '__main__':
    main()