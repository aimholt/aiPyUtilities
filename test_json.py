from aiPyUtilsPack.general import get_object_summary
import json
import os

DIR='/home/andreas/projects/testData'
FILE='testdata.json'

raw0 ='''
[
    1,
    2,
    "a",
    3,
    4,
    {"a": 1,"b": 2},
    {"a": 1,"b": 2},
    {"a": 1,"b": 2},
    {"a": 1,"b": 2,"c":["x",2,true,4]},
    "7"
]
'''
raw1 ='''
[
  {"y": 3, "x": 4},
  {"a": 1, "b": 2},
  {"a": "text", "b": 4.5},
  {"a": 3, "b": 4},
  {"x": [1, 2], "y": "ok"},
  {"x": [3, 4], "y": "ok"}
]
'''
raw2 ='''
[
    {"x": [1, 2], "y": "ok"},
    {"x": ["a", "b"], "y": "ok"},
    {"x": [], "y": "empty"},
    {"x": [{"a":1}], "y": "dict_in_list"}
]
'''

raw4='''
[1,2,3,4,5]
'''
raw5='''
[9,["a","b",["-",6,"#"],"d"],"1","2",3,["a",1],"5"]
'''
raw6='''
[9,"2",["a",2,"c"],"3","4",5,"6"]
'''
raw7='''
[1,2,{"a":1, "b":2},{"a":1, "b":2},{"a":1, "b":2},{"a":1, "b":2, "c": ["x","y","z"]},7]
'''
raw8='''
{"a":{"a":1,"b":{"a":1,"b":2}},"b":{"a":1,"b":4}}
'''
raw9='''
{"a":1,"b":2,"c":3}
'''
raw10='''
{
  "pid": "log",
  "hide": {
    "mobile": true,
    "liveTv": true,
    "tfa": true,
    "ssoSet": true,
    "rrd": true
  },
  "timeTillLogout": "1200",
  "time": [],
  "data": {
    "show": {
      "usb": true,
      "wlan": {
        "has_5ghz_band": true,
        "has_wpa2_support": true,
        "is_double_wlan": true,
        "is_triband": false,
        "has_6ghz_band": false,
        "is_dbdc": true
      },
      "net": true,
      "all": true,
      "fon": true,
      "sys": true
    },
    "log": [
      {
        "helplink": "/help/help.lua?sid=7a7f8b9cc442696b&helppage=hilfe_syslog_504.html",
        "time": "23:06:16",
        "group": "sys",
        "id": 504,
        "msg": "Anmeldung des Benutzers aimholt an der FRITZ!Box-Benutzeroberflache von IP-Adresse 192.168.1.58.",
        "date": "01.10.25",
        "nohelp": 1
      },
      {
        "helplink": "/help/help.lua?sid=7a7f8b9cc442696b&helppage=hilfe_syslog_754.html",
        "time": "22:51:44",
        "group": "wlan",
        "id": 754,
        "msg": "[xyzRepeater1] WLAN-Gerat wurde abgemeldet (5 GHz), iPhone, IP 192.168.1.48, MAC AE:00:E0:62:4F:FE.",
        "date": "01.10.25",
        "nohelp": 0
      },
      {
        "helplink": "/help/help.lua?sid=7a7f8b9cc442696b&helppage=hilfe_syslog_30005.html",
        "time": "22:46:44",
        "group": "wlan",
        "id": 30005,
        "msg": "WLAN-Gerat angemeldet (5 GHz), 866 Mbit/s, mobile-ai, IP 192.168.1.48, MAC AE:00:E0:62:4F:FE.",
        "date": "01.10.25",
        "nohelp": 1
      },
      {
        "helplink": "/help/help.lua?sid=7a7f8b9cc442696b&helppage=hilfe_syslog_30005.html",
        "time": "22:46:44",
        "grfoup": "wlan",
        "id": 30005,
        "msg": "WLAN-Gerat angemeldet (5 GHz), 866 Mbit/s, mobile-ai, IP 192.168.1.48, MAC AE:00:E0:62:4F:FE.",
        "date": "01.10.25",
        "nohelp": 1
      }
    ],
    "filter": "all",
    "wlanGuestPushmail": true,
    "wlan": true
  },
  "sid": "7a7f8b9cc442696b",
  "blub":{
    "keyA":  "dfkldfk",
    "keyB":  "dfkldfk"
  }
}
'''

with open(DIR+os.sep+FILE,'r', encoding='UTF-8') as f:
    data_py=json.load(f)
#data_py=json.loads(raw8)
for item in get_object_summary(data_py):
    print(item)