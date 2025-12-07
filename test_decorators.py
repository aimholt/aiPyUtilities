
import time
import random
import sys
from aiPyUtilsPack.general import get_runtime
def sleep_a_while():
    print('sleep_a_while')
    time.sleep(random.randint(1,3))

@get_runtime
def sleep_so_long(n):
    """ 
        testing the decorator functionality
    """
    print(f'Anwendung läuft({sys.argv[0]})')
    time.sleep(n)
def sleep_not_much(stay_awake=False):
    if not stay_awake:
        time.sleep(0.1)

####alternative to decorators is the following(same function call)
#leep_so_long=get_runtime(sleep_so_long)

#sleep_a_while()
#sleep_not_much(stay_awake=True)
sleep_so_long(2)
