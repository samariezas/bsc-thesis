import os
import os.path
import re
import numpy as np
import matplotlib.pyplot as plt

GUEST_RESULTS = './guest-combined/'
HOST_RESULTS = './host/'
NUMBER_FINDER = re.compile('[0-9]+')


def load_results(path):
    retval = {}
    currently_loaded = set()
    for fname in os.listdir(path):
        qbits, = (int(i) for i in NUMBER_FINDER.findall(fname))
        assert qbits not in currently_loaded
        currently_loaded.add(qbits)
        fname = os.path.join(path, fname)
        if os.path.isfile(fname):
            with open(fname, 'r') as f:
                lines = [l for l in f.readlines() if 'Time taken' in l]
                if not lines:
                    print(f'W: skipping {fname}')
                    continue

                for line in lines:
                    time_split = line.split(':')
                    assert len(time_split) == 2
                    seconds_taken = int(time_split[1].strip()) / 1e9
                    if qbits not in retval:
                        retval[qbits] = []
                    retval[qbits] += [seconds_taken]
    return retval


if __name__ == '__main__':
    guest_results = load_results(GUEST_RESULTS)
    host_results = load_results(HOST_RESULTS)
    for qbits in range(12, 17):
        guest = np.array(guest_results[qbits], dtype=np.float64)
        host = np.array(host_results[qbits], dtype=np.float64)
        arr = host
        mean = np.mean(arr)
        dev = np.std(arr)
        print(arr)
        print(mean, dev)
        # plt.hist(arr, bins=32, range=(mean - 2*dev, mean + 2*dev))
        plt.hist(arr, bins=64)
        plt.show()
        # print(f'{np.std(guest)=}, {np.mean(guest)=}')
        # print(f'{np.std(host)=}, {np.mean(host)=}')
