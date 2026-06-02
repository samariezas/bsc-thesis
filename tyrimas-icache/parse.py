import os
import os.path
import re
import numpy as np
import matplotlib
matplotlib.use("pgf")
matplotlib.rcParams.update({
    "pgf.texsystem": "lualatex",
    "text.usetex": True,
    "font.family": "serif",
})
import matplotlib.pyplot as plt

NUMBER_FINDER = re.compile('[0-9]+')

def load_results(path):
    retval = {}
    currently_loaded = set()
    for fname in os.listdir(path):
        if not fname.endswith('txt'):
            continue
        if os.path.isfile(fname):
            name, _ = fname.split('.')
            assert name not in currently_loaded
            currently_loaded.add(name)
            fname = os.path.join(path, fname)
            with open(fname, 'r') as f:
                lines = [l for l in f.readlines() if 'real' in l]
                if not lines:
                    print(f'W: skipping {fname}')
                    continue

                for line in lines:
                    _, time_split = line.split('\t')
                    minutes, seconds = (t.strip() for t in time_split.split('m'))
                    print(seconds)
                    assert seconds[-1] == 's'
                    seconds = seconds[:-1]
                    minutes = float(minutes)
                    seconds = float(seconds)
                    if name not in retval:
                        retval[name] = []
                    retval[name] += [minutes * 60 + seconds]
    return retval


def gen_row(name, results):
    mean = np.mean(results)
    std = np.std(results)
    # p5, p95 = np.percentile(results, [5, 95])
    # return f'{name} & {mean} & {std} & {p5} & {p95} \\\\'
    return f'{name} & {mean:.3f} & {std:.3f} \\\\'


if __name__ == '__main__':
    results = load_results('./')
    array_plot = []
    for k, v in results.items():
        print(k, np.mean(v))
        ARRAY_START = 'array-'
        if k.startswith(ARRAY_START):
            arr_len = int(k[len(ARRAY_START):])
            p5 = np.percentile(v, 5)
            mean = np.mean(v)
            p95 = np.percentile(v, 95)
            array_plot += [(arr_len, mean, p5, p95)]

    array_plot = np.array(sorted(array_plot))
    x = array_plot[:, 0]
    y = array_plot[:, 1]
    # p5 = array_plot[:, 2]
    # p95 = array_plot[:, 3]
    fig, ax = plt.subplots()
    ax.plot(x, y)
    ax.set_xlabel('Talpyklos dydis')
    ax.set_ylabel('Vidutinis vykdymo laikas, s')
    ax.axis()
    # fig.fill_between(x, p5, p95, alpha=0.3, label='5th-95th percentile')
    ax.set_xscale('log')
    fig.savefig('./array.pgf')

    with matplotlib.rc_context({
        "font.size": 14,
        "axes.labelsize": 14,
        "xtick.labelsize": 8,
        "ytick.labelsize": 8,
    }):
        ax.plot(x, y, marker='x', color='blue', linewidth=0.8)
        ax.set_xlabel('Talpyklos dydis', fontsize=6)
        ax.set_ylabel('Vidutinis vykdymo laikas, s', fontsize=6)
        fig.set_size_inches(2.8, 2)
        fig.tight_layout()
        ax.set_title("", pad=0)
        fig.savefig('./array-smaller.pgf', bbox_inches='tight', pad_inches=0)

    # std_none = np.std(results['none'])
    # std_hashmap = np.std(results['hashmap'])
    # std_array = np.std(results['array-1048573'])

    lines = [
        gen_row('Be talpyklos', results['none']),
        gen_row('Maišos lentelė', results['hashmap']),
        gen_row('Masyvas, $N = 1048573$', results['array-1048573'])
    ]
    print('\n\\hline\n'.join(lines))
