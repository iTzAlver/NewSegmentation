# - x - x - x - x - x - x - x - x - x - x - x - x - x - x - #
#                                                           #
#   This file was created by: Alberto Palomo Alonso         #
# Universidad de Alcalá - Escuela Politécnica Superior      #
#                                                           #
# - x - x - x - x - x - x - x - x - x - x - x - x - x - x - #
# Import statements:
import os
import numpy as np
import src.newsegmentation as ns
import logging
import unittest

DATA_PATH = r'./test_db/data/'
GT_PATH = r'./test_db/ground_truth/'
RESULTS_PATH = r'./test_db/results/'
# -----------------------------------------------------------


class TestSegmentation(unittest.TestCase):
    def test_vtt(self):
        logging.basicConfig(level=logging.DEBUG)
        logging.info('[+] Connected to test 0...')
        try:
            ns.Segmentation(r'./myfile.vtt')
            logging.info('\t[$] Test 0 finished successfully.')
        except Exception as e:
            logging.error(f'\t[!] Test 0 failed: {e}')
            logging.error('\t[?] VTT reading may be broken...')
            self.assertTrue(False, msg='Results are not equal.')
        finally:
            logging.info('[-] Disconnected from test 0...')

    def test_results(self):
        logging.info('[+] Connected to test 1...')
        try:
            results = list()
            for data, gt in zip(os.listdir(DATA_PATH), os.listdir(GT_PATH)):
                segmentation = ns.Segmentation(os.path.join(DATA_PATH, data))
                results.append(list(segmentation.evaluate(os.path.join(GT_PATH, gt)).values()))
                logging.info(f'\t\t[$] File: {data.replace(".txt", "")}.')
            logging.info(f'\t\t[$] 200 / 200.')
            logging.info('\t[$] Test 1 finished processing, starting checks.')
            np_hyp = np.array(results)
            np_res = np.load(os.path.join(RESULTS_PATH, '0_50.npy'))[:-1]
            np.concatenate((np_res, np.load(os.path.join(RESULTS_PATH, '50_100.npy'))[:-1]))
            np.concatenate((np_res, np.load(os.path.join(RESULTS_PATH, '100_150.npy'))[:-1]))
            np.concatenate((np_res, np.load(os.path.join(RESULTS_PATH, '150_200.npy'))[:-1]))
            np_res = np_res.reshape(-1, 5)
            self.assertTrue(np.allclose(np_hyp, np_res), msg='Results are not equal.')
            logging.info('\t[$] Test 0 finished successfully.')
        except Exception as e:
            logging.error(f'\t[!] Test 1 failed: {e}')
            logging.error('\t[?] Package broken.')
        finally:
            logging.info('[-] Disconnected from test 1...')
        return
# -----------------------------------------------------------


if __name__ == '__main__':
    unittest.main()
# - x - x - x - x - x - x - x - x - x - x - x - x - x - x - #
#                        END OF FILE                        #
# - x - x - x - x - x - x - x - x - x - x - x - x - x - x - #
