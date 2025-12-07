from typing import Any, Dict, List, Tuple
from collections import Counter
from itertools import groupby
import time
from functools import wraps

def _type_name(value: Any) -> str:
    """
        returns a short type name
    """
    if value is None:
        ret="None"
    elif isinstance(value, bool):
        ret="bool"
    elif isinstance(value, int):
        ret="int"
    elif isinstance(value, float):
        ret="float"
    elif isinstance(value, str):
        ret="str"
    elif isinstance(value, dict):
        ret="dict"
    elif isinstance(value, list):
        ret="list"
    else:
        ret="?-?"
    return ret

def _obj_signature(d: List|Dict[str, Any])  -> Tuple[str, ...]:
    """ return a signature tuple for dict or list type """
    ret=None
    if isinstance(d, list):
        list_struct = []
        for key, group in groupby(d, key=_type_name):
            count = len(list(group))
            list_struct.append(f"{key}({count}x)")
        ret=tuple(list_struct)
    elif isinstance(d, dict):
        ret=tuple(f"{k}: {_type_name(v)}" for k, v in d.items())
    return ret

def _obj_struct(obj: List|Dict, level=0, name:str = '', counter: Counter=None):
    """
        returns a counter type with tuples that represents a an element structure
    """
    if counter is None:
        counter = Counter()
    sig_plus=(int(level),name,_type_name(obj))+_obj_signature(obj)
    counter[sig_plus]+=1
    if type(obj) == dict:
        for key, value in obj.items():
            if type(value) == dict or type(value) == list:
                level+=1
                _obj_struct(value, level=level, name=key, counter=counter)
                level-=1
        level-=1
    elif type(obj) == list:
        for item in obj:
            if  type(item) == dict or type(item) == list:
                level+=1
                _obj_struct(item, level=level, name='ListItem', counter=counter)
                level-=1    
    return counter

def get_object_summary(obj: Any) -> List:
    """
        returns a list the structure of a complex object
        i.e. for analyse the large json structure converted by json.loads()
    """
    ret=[]
    header="Summary of object structure"
    trailer="="*len(header)
    ret.append(f'\n{header}\n'+'='*len(header))
    for k, v in _obj_struct(obj).items():
        label=f'L{str(k[0])}{"   "*k[0]}'
        if k[0]==0:
            ret.append(f'{label} {k[2]} with {k[3:]} ->({v}x)')
        else:
            ret.append(f'{label}<{k[1]}> {k[2]} with {k[3:]} ->({v}x)')
    ret.append(f'{trailer}')
    return ret

def get_runtime(fn):
    """
        Decorator function to get the runtime of an executed function
    """
    @wraps(fn)    ### makes, that '__name__' and  '__doc__' keeps original values 
    def wrapper(*args, **kwargs):
        """
            generic wrapper(with generic parameters) to get the runtime for a function
            parameters can be more specific but has to fit to all functions the wrapper 
            will be used for
        """        
        start_time = time.perf_counter()
        try:
            ### calling the function with the arguments
            return (fn(*args, **kwargs))
        finally:
            end_time = time.perf_counter()
            print(f'runtime of {fn.__name__}: {(end_time - start_time):.3f}')
    return wrapper