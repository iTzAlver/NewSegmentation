# - x - x - x - x - x - x - x - x - x - x - x - x - x - x - #
#                                                           #
#   This file was created by: Alberto Palomo Alonso         #
# Universidad de Alcalá - Escuela Politécnica Superior      #
#                                                           #
# - x - x - x - x - x - x - x - x - x - x - x - x - x - x - #
# Import statements:
import logging
import requests
import os
import bs4
__wikipedia_random_path__ = 'https://es.wikipedia.org/wiki/Special:Random'


# - # - # - # - # - # - # - # - # - # - # - # - # - # - # - #
def main() -> None:
    return


# - # - # - # - # - # - # - # - # - # - # - # - # - # - # - #


class ReadDatabase:
    def __init__(self, number_of_data: int, data_path: str, gt_path: str,
                 p: tuple = (1., 0.), minimum_words: int = 10, max_block_len: int = 20, data_modeling: tuple = (30, 4)):
        """
        This class generates a dataset for testing the Topic Segmentation feature of the architecture.
        :param number_of_data: Number of data instances to generate. [files]
        :param data_path: Data storage path. [str]
        :param gt_path: Ground truth path. [str]
        :param p: Probability of detection and false detection of the temporal jumps. [non-dimensional]
        :param minimum_words: The minimum words for a block to be computed. [words]
        :param max_block_len: The maximum length of a segmentation boundary. [sentences]
        :param data_modeling: The mean and variance of the number of sentences in one file. [mean, variance]
        """
        # Create or check the current data folders:
        if not os.path.exists(data_path):
            os.mkdir(data_path)
        if not os.path.exists(gt_path):
            os.mkdir(gt_path)
        length_of_data = len(os.listdir(data_path))
        length_of_grth = len(os.listdir(data_path))
        if not length_of_grth == length_of_data:
            _error_msg = 'Error while importing the current database: the ground truth does not match the data lenght'
            logging.error(_error_msg)
            raise ValueError(_error_msg)

        # Check the probability of temporal jump detection:
        if not 0 <= p[0] <= 1 or not 0 <= p[1] <= 1:
            _error_msg = 'Error while importing the current database: ' \
                         'the probabilities must be lower than 1 and positive.'
            logging.error(_error_msg)
            raise ValueError(_error_msg)

        # Check other parameters:
        if number_of_data <= 0:
            _error_msg = 'The number of data must be positive.'
            logging.error(_error_msg)
            raise ValueError(_error_msg)
        if max_block_len <= 0:
            _error_msg = 'The max block length of the data must be positive.'
            logging.error(_error_msg)
            raise ValueError(_error_msg)
        if minimum_words <= 0:
            _error_msg = 'The minimum number of words must be positive.'
            logging.error(_error_msg)
            raise ValueError(_error_msg)
        if data_modeling[0] <= 0 or data_modeling[1] <= 0:
            _error_msg = 'The mean and variance of the data modeling be positive.'
            logging.error(_error_msg)
            raise ValueError(_error_msg)

        self.current_index = length_of_data  # Or length_of_grth.
        self.minimum = minimum_words  # The minimum number of words of a block to become a valid sentence.
        self.maximum = max_block_len
        self.p = p
        self.mean = data_modeling[0]
        self.variance = data_modeling[1]

    @staticmethod
    def _read_block() -> list[tuple[int, str]]:
        # Obtain the text from the random URL.
        response = requests.get(__wikipedia_random_path__, headers={'User-Agent': 'Mozilla/5.0'})
        soup = bs4.BeautifulSoup(response.text, features="html.parser")
        text_list = soup.body.get_text().split('\n')
        _text_list = [(0, ''), (0, '')]
        for _text_ in text_list:
            _nwords = len(_text_.split(' '))
            _text_list.append((_nwords, _text_))
        _text_list.sort(key=lambda x: x[0], reverse=True)
        return [text for _, text in _text_list]

    @staticmethod
    def __preprocess_string(lines: list[str], minimum_words: int):
        _return_lines_ = []
        for line in lines:
            if 'Categorías:' not in line and '↑' not in line:
                _return_line_ = line
                _return_line_ = _return_line_.replace(' ', '').replace('   ', ' ').replace('    ', ' ')\
                    .replace('  ', ' ').replace('»', '"').replace('«', '"').replace(' ', '').replace(' ', '').\
                    replace('\u200b', '')
            else:
                _return_line_ = ''
            if len(_return_line_.split(' ')) > minimum_words:
                _return_line_ = _return_line_.replace('...', '↑. ')
                _return_sentences_ = [sentence.replace('↑', '...') for sentence in _return_line_.split('. ')]
                _return_lines_.append(_return_sentences_)
        return _return_lines_
# - # - # - # - # - # - # - # - # - # - # - # - # - # - # - #


if __name__ == "__main__":
    main()
# - x - x - x - x - x - x - x - x - x - x - x - x - x - x - #
#                        END OF FILE                        #
# - x - x - x - x - x - x - x - x - x - x - x - x - x - x - #
