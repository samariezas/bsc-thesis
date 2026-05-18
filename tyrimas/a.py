import os
import os.path
import re
import numpy as np
import matplotlib.pyplot as plt

GUEST_RESULTS = './guest2/'
HOST_RESULTS = './host2/'
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


def do_plot(ax, name, data, dev=None):
    mean = np.mean(data)
    if dev is None:
        dev = np.std(data)
    print(f'{name:10} | {mean:8.4f} | {np.std(data):14.10f} |')
    ax.set_title(name)
    ax.hist(data, bins=32, range=(mean - 2*dev, mean + 2*dev))


if __name__ == '__main__':
    guest_results = load_results(GUEST_RESULTS)
    host_results = load_results(HOST_RESULTS)
    k1 = sorted(list(guest_results.keys()))
    k2 = sorted(list(host_results.keys()))
    assert k1 == k2
    keys = k1

    for qbits in keys:
        guest = np.array(guest_results[qbits], dtype=np.float64)
        host = np.array(host_results[qbits], dtype=np.float64)

        dev = max(np.std(guest), np.std(host))

        m_guest = np.mean(guest)
        m_host = np.mean(host)
        diff = m_guest / m_host
        # print(f'diff: {diff}')

        print(f'{qbits:10} & {m_host:8.4f} & {m_guest:8.4f} & {diff:8.4f}')

        # fig, (ax1, ax2) = plt.subplots(1, 2)
        # do_plot(ax1, f'host-{qbits}', host, dev=dev)
        # do_plot(ax2, f'guest-{qbits}', guest, dev=dev)
        # plt.show()
