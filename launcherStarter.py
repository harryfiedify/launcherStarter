#!/usr/bin/env python

import yaml
import time
import psutil
import os
import sys

defaults=dict()

class activityMeter:
    def __init__(self,func):
        self.__func = func

        self.__prev_time = time.time()
        self.__prev_val = self.__func()
        
    
    def get_rate(self):
        cur_val = self.__func()
        cur_time = time.time()

        result = (cur_val-self.__prev_val)/(cur_time-self.__prev_time)

        self.__prev_time = cur_time
        self.__prev_val = cur_val

        return result

class rollingAvg:
    def __init__(self,length):
        self.__vals=[]
        self.__length=length

    def put(self,in_val):
        self.__vals.append(in_val)
        if len(self.__vals)>self.__length:
            self.__vals.pop(0)
        # print(self.__vals)
        return self.get()
    
    def get(self):
        return sum(self.__vals)/len(self.__vals)

def cmd_sleep(length):
    for i in range(length,0,-1):
        print("Waiting {:3} seconds".format(i), end="\r")
        time.sleep(1)

def prevent_sleep(enable=True):
    # https://stackoverflow.com/questions/57647034/prevent-sleep-mode-python-wakelock-on-python 
    # https://superuser.com/questions/146729/whats-keeping-my-computer-awake 
    import ctypes
    if enable:
        ctypes.windll.kernel32.SetThreadExecutionState(0x80000002)
    else:
        ctypes.windll.kernel32.SetThreadExecutionState(0x80000000)

def waitlim(dSet):
    # init
    dSet.update({
        'network-avg': rollingAvg(dSet['network-length']),
        'disk-avg': rollingAvg(dSet['disk-length']),
        'cpu-avg': rollingAvg(dSet['cpu-length']),
        'starttime': time.time()
    })
    network=activityMeter(lambda :psutil.net_io_counters().bytes_recv/1024)
    disk = activityMeter(lambda :psutil.disk_io_counters().read_bytes/1024+psutil.disk_io_counters().write_bytes/1024)
    cpu = lambda :psutil.cpu_percent()

    # https://stackoverflow.com/questions/287871/how-to-print-colored-text-to-the-terminal 
    cRed=' \x1b[0;37;41m'
    cGreen=' \x1b[0;37;42m'
    cEnd='\x1b[0m '


    # wait loop breaks when all conditions are fulfilled (waitlock==0)
    while ( True ):
        waitlock=0
        if dSet['network']:
            temp=dSet['network-avg'].put(network.get_rate())
            if temp>dSet['network-limit']:
                print(cRed, end='')
                waitlock += 1
            else:
                print(cGreen, end='')
            print('NET {:.1f} kb/s'.format(temp) + cEnd, end='')

        if dSet['disk']:
            temp=dSet['disk-avg'].put(disk.get_rate())
            if temp>dSet['disk-limit']:
                print(cRed, end='')
                waitlock += 1
            else:
                print(cGreen, end='')
            print('DISK {:.1f} kb/s'.format(temp) + cEnd, end='')

        if dSet['cpu']:
            temp=dSet['cpu-avg'].put(cpu())
            if temp>dSet['cpu-limit']:
                print(cRed, end='')
                waitlock += 1
            else:
                print(cGreen, end='')
            print('CPU {:.1f} %'.format(temp) + cEnd, end='')
        
        if dSet['time']>0:
            temp=round(dSet['starttime']+dSet['time']-time.time(),1)
            if temp>0:
                print(cRed, end='')
                waitlock += 1
            else:
                print(cGreen, end='')
                temp=0 # avoid showing negative time
            print('TIME {:.1f} s'.format(temp) + cEnd, end='')

        if dSet['timeout']>0 and dSet['starttime']+dSet['timeout']<time.time():
            print(cRed+"TIMEOUT"+cEnd, end='')
            waitlock=0

        if waitlock <= 0: # end while
            print('') # new line
            break
        else:
            print('',end='\r') # reset to beginning of line
            time.sleep(1)

def read_config(fname):
    global defaults
    with open(fname,'r') as ymlfile:
        temp_cfg = yaml.safe_load(ymlfile)
    defaults.update(temp_cfg['defaults'])
    return temp_cfg['recipe']


def main():
    print("### launcherStarter.py ###")
    print("Press Ctrl-C to stop")
    
    if len(sys.argv)<2: # no config file supplied, using default
        print('reading ./config.yml')
        recipe=read_config('./config.yml')
    else:
        print('reading '+sys.argv[1])
        recipe=read_config(sys.argv[1])

    prevent_sleep(True) # stops automatically after process exit
    
    for l in recipe:
        if "wait" in l:
            #print('waiting')
            dWait = defaults['wait'].copy()
            if l['wait'] != None:
                dWait.update(l['wait'])
            #print(dWait)
            waitlim(dWait)
        elif "launch" in l:
            print('')
            print('launching '+l['launch']['name'])
            #print(l['launch'])
            os.popen('start '+l['launch']['path'])






if __name__ == '__main__':
    os.system('color') # make colors work in CMD
    os.system('title '+sys.argv[0])
    main()