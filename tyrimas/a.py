import os
import os.path
import re
import numpy as np
import matplotlib.pyplot as plt

GUEST_RESULTS = './guest-results/'
HOST_RESULTS = './host-results/'
NUMBER_FINDER = re.compile('[0-9]+')


def load_results(path):
    retval = {}
    currently_loaded = set()
    for fname in os.listdir(path):
        qbits, iter_id = (int(i) for i in NUMBER_FINDER.findall(fname))
        assert (qbits, iter_id) not in currently_loaded
        currently_loaded.add((qbits, iter_id))
        fname = os.path.join(path, fname)
        if os.path.isfile(fname):
            with open(fname, 'r') as f:
                line = [l for l in f.readlines() if 'Time taken' in l]
                if not line:
                    print(f'W: skipping {fname}')
                    continue
                assert len(line) == 1
                time_split = line[0].split(':')
                assert len(time_split) == 2
                seconds_taken = int(time_split[1].strip()) / 1e9
                if qbits not in retval:
                    retval[qbits] = []
                retval[qbits] += [seconds_taken]
    print(retval)
    return retval


if __name__ == '__main__':
    results = load_results('./libquantum-results-better')
    # guest_results = load_results(GUEST_RESULTS)
    # host_results = load_results(HOST_RESULTS)
    for qbits in range(12, 17):
        # guest = np.array(guest_results[qbits], dtype=np.float64)
        # host = np.array(host_results[qbits], dtype=np.float64)
        # plt.hist(guest)
        arr = results[qbits]
        mean = np.mean(arr)
        dev = np.std(arr)
        print(mean, dev)
        plt.hist(results[qbits], bins=32, range=(mean - 2*dev, mean + 2*dev))
        plt.show()
        # print(f'{np.std(guest)=}, {np.mean(guest)=}')
        # print(f'{np.std(host)=}, {np.mean(host)=}')
