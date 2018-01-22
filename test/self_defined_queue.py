"""
Self defined queue
"""

import threading
import time


def sleeper(n, name):
    print('Hi, I am {}.'.format(name) +'Going to sleep for {} seconds \n'.format(name))
    time.sleep(n)
    print('{} has woken up from sleep \n'.format(name))



thread_list = []
for i in range(5):
    t = threading.Thread(target=sleeper,
                         name='thread{}'.format(i),
                         args=(i+1, 'thread{}'.format(i)))
    thread_list.append(t)

start = time.time()
for i in thread_list:
    i.start()

print(time.time()-start)

print("something else")