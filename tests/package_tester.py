# - x - x - x - x - x - x - x - x - x - x - x - x - x - x - #
#                                                           #
#   This file was created by: Alberto Palomo Alonso         #
# Universidad de Alcalá - Escuela Politécnica Superior      #
#                                                           #
# - x - x - x - x - x - x - x - x - x - x - x - x - x - x - #
# Import statements:
import time
import numpy as np
import os
import src.newsegmentation as ns

from_which = 0
max_files = 10
__data_path__ = 'C:\\Users\\ialve\\Desktop\\NewSegmentation\\topic_segmentation\\database\\data'
__gt_path__ = 'C:\\Users\\ialve\\Desktop\\NewSegmentation\\topic_segmentation\\database\\ground_truth'
data_paths = [f'{__data_path__}\\{one}' for one in os.listdir(__data_path__)][from_which:max_files]
gt_paths = [f'{__gt_path__}\\{one}' for one in os.listdir(__gt_path__)][from_which:max_files]


# -----------------------------------------------------------
def validation() -> None:
    mns = ns.Segmentation(r'./myfile.vtt')
    print(mns)
    ns.info()
    ns.about()
    mns.plotmtx(0, 1, 2, 3)
    for news in mns:
        print(news)


if __name__ == '__main__':
    validation()
# - x - x - x - x - x - x - x - x - x - x - x - x - x - x - #
#                        END OF FILE                        #
# - x - x - x - x - x - x - x - x - x - x - x - x - x - x - #
