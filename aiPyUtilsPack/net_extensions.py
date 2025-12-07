"""
    functions for network processing
"""
import re

def valid_ip(address):
    """
        validate a given IP address
    """
    p=re.compile('^(\\d{1,3})\\.(\\d{1,3})\\.(\\d{1,3})\\.(\\d{1,3})$')
    m=p.match(address)
    valid=True
    if m:
        for i in range(1,5):
            if int(m.group(i)) > 255: #checking all octets if valid range
                valid=False
            elif m.group(i).startswith('0'):
                valid=False
    else:
        valid=False
    return valid
