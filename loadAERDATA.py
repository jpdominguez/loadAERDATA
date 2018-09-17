import struct
import numpy as np


def checkAERDATA(p_timestamps, p_number_of_addresses =  -1, p_events = []):

    # Check all timestamps are greater than zero
    a = all(item >= 0  for item in p_timestamps)

    # Check every timestamp is greater than its previous one
    b = any(i > 0 and p_timestamps[i] < p_timestamps[i-1] for i in range(len(p_timestamps)))

    # Check all addresses are between zero and the total number of addresses
    c = all(item >= 0 and item < p_number_of_addresses for item in p_events)

    return a and not b and c 
            

def adaptAERDATA(p_timestamps, p_tick):
    return [(x - p_timestamps[0])*p_tick for x in p_timestamps]


def loadAERDATA(p_path, p_address_size = 2):
    events = []
    timestamps = []
    unpack_param = ">H"
    
    if p_address_size == 2:
        unpack_param = ">H"
    elif p_address_size == 4:
        unpack_param = ">L"
    else:
        print "Only address sizes implemented are 2 and 4 bytes"

    with open(p_path, 'rb') as f:
        while True:
            buff = f.read(p_address_size)
            if len(buff) < p_address_size: break
            x = np.uint16(struct.unpack(unpack_param, buff)[0])
            events.append(x)

            buff = f.read(4)
            if len(buff) < 4: break
            x = struct.unpack('>L', buff)[0]
            timestamps.append(x)
    return events, timestamps






path = 'C:\\Users\\jpdominguez\\Desktop\\test_aedat\\sample_AERDATA.aedat'

[add, ts] = loadAERDATA(path)

print len(add)
print len(ts)

print add[0]
print ts[0]

ts = adaptAERDATA(ts, 0.2)

print ts[-1]

print checkAERDATA(ts, 64, add)