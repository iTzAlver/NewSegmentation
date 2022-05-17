# - x - x - x - x - x - x - x - x - x - x - x - x - x - x - #
#                                                           #
#   This file was created by: Alberto Palomo Alonso         #
# Universidad de Alcalá - Escuela Politécnica Superior      #
#                                                           #
# - x - x - x - x - x - x - x - x - x - x - x - x - x - x - #
import numpy as np


def ftdm(p, s, slm, betta):
    r = slm(s)
    _p = p.copy()
    _p.append(len(r))
    r1 = np.zeros((len(r), len(r)))
    for nr, row in enumerate(r1):
        for nc, _ in enumerate(row):
            join = True
            for tid, placeholder in enumerate(_p):
                pid = _p[tid - 1] if tid > 0 else 0
                if nr in range(pid, placeholder) and nc in range(pid, placeholder):
                    join = False
            r1[nr][nc] = (1 - betta)*r[nr][nc] if join else r[nr][nc]
    return r, r1
# - x - x - x - x - x - x - x - x - x - x - x - x - x - x - #
#                        END OF FILE                        #
# - x - x - x - x - x - x - x - x - x - x - x - x - x - x - #
