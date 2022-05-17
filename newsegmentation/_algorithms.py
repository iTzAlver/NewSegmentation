# - x - x - x - x - x - x - x - x - x - x - x - x - x - x - #
#                                                           #
#   This file was created by: Alberto Palomo Alonso         #
# Universidad de Alcalá - Escuela Politécnica Superior      #
#                                                           #
# - x - x - x - x - x - x - x - x - x - x - x - x - x - x - #
# Import statements:
import numpy as np


# -----------------------------------------------------------
def pbmm(r, param):
    # Parameter check:
    if len(param) == 3:
        th = param[0]
        oim = param[1]
        cbt = param[2]
    else:
        raise Exception(f'Invalid parameters in PBMM algorithm: {len(param)} given 3 expected.')

    # Variable initialization:
    failure_counter = 0
    last_index = -1
    current_index = 0
    appindex = 0
    d = []

    # Algorithm loop:
    while (current_index := current_index + 1) < len(r):
        # Compute mean
        elements = r[current_index][last_index+1:current_index]
        if current_index - last_index - 1 <= 0:
            mean = 1
        else:
            mean = sum(elements) / (current_index - last_index - 1)
        # Algorithm control:
        if mean < th:
            failure_counter += 1
        else:
            appindex = current_index
            failure_counter = 0

        if failure_counter > oim:
            d.append(appindex + 1)
            len_cb = d[-1] - last_index - 1     # Checkback init.
            init_cb = last_index + 1            # Checkback init.
            last_index = appindex
            current_index = appindex

            # Checkback...
            if len_cb > 1:
                cb_mean = 0
                for i in range(len_cb - 1):
                    cb_mean += r[init_cb][init_cb + i + 1]
                cb_mean /= (len_cb - 1)
                if cb_mean < cbt:
                    # Check back integrity...
                    cb_mean_back = r[init_cb][init_cb - 1] if init_cb > 0 else -1
                    if cb_mean_back < cbt:
                        aux = d.pop(-1)
                        d.append(d[-1] + 1)
                        d.append(aux)
                    else:
                        d[-2] += 1
    # Last element:
    d.append(current_index)
    return d


def fbbcm(lm, s, t, param):
    th = param[0]
    popping = [-1]
    this_s = s
    this_t = t
    r = []
    while popping:
        r = lm(this_s)
        indexing = []
        for nr, row in enumerate(r):
            _row = [element if (th < element and nr != nc) else 0 for nc, element in enumerate(row)]
            mxval = max(_row)
            indexing.append(_row.index(mxval) if mxval >= th else -1)

        popping = []
        for nidx, idx in enumerate(indexing):
            if indexing[idx] == nidx and nidx > idx != -1:
                this_s[nidx] = f'{this_s[nidx]}. {this_s[indexing[idx]]}'
                this_t[nidx] += this_t[indexing[idx]]
                popping.append(indexing[idx])

        popping.sort(reverse=True)
        for popp in popping:
            this_s.pop(popp)
            this_t = np.delete(this_t, popp)

    return r, this_s, this_t
# - x - x - x - x - x - x - x - x - x - x - x - x - x - x - #
#                        END OF FILE                        #
# - x - x - x - x - x - x - x - x - x - x - x - x - x - x - #
