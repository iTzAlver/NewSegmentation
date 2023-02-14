# - x - x - x - x - x - x - x - x - x - x - x - x - x - x - #
#                                                           #
#   This file was created by: Alberto Palomo Alonso         #
# Universidad de Alcalá - Escuela Politécnica Superior      #
#                                                           #
# - x - x - x - x - x - x - x - x - x - x - x - x - x - x - #
# Import statements:
import time
import requests
import numpy as np
from bs4 import BeautifulSoup
# - # - # - # - # - # - # - # - # - # - # - # - # - # - # - #


class WikipediaReader:
    def __init__(self, number_of_articles: int = 1, p: tuple[float, float] = (.8, 0.05), max_block_len: int = 12):
        """
        This class reads a random article from Wikipedia. The article is stored in the self.article attribute, and it
        is parsed by the class automatically.
        :param number_of_articles: The number of articles to read. [articles]
        :param p: The probability of detection and false detection of the temporal jumps. [non-dimensional]
        :param max_block_len: The maximum length of the temporal jump. [sentences]
        """
        self.url = 'https://es.wikipedia.org/wiki/Special:Random'
        self.prob_true_detection = p[0]
        self.prob_fake_detection = p[1]
        self.max_block_len = max_block_len
        # Read the article:
        self.article: list = self.__read_article(number_of_articles)
        # Split the article into sentences:
        try:
            sentences, residual = self.__split_into_sentences_and_add(self.article)
            self.sentences_article = sentences
            self.sentences_article.extend(residual)
            self.sentences_gt = self.__split_into_sentences_only(self.article)
            if self.__validation(self.sentences_gt, self.sentences_article):
                print('WikipediaReader: The validation was successful.')
                self.success = True
            else:
                print('WikipediaReader: The validation was not successful.')
                self.success = False
        except IndexError:
            print('WikipediaReader: The article is empty.')
            self.success = False
            time.sleep(1)
            return

    def save(self, path: str = '', index: int = 0) -> None:
        """
        This method saves the sentences article in the path directory like a .txt file.
        This method also saves the sentences gt in the path directory like a .gt file.
        The index tells the name of the file.
        :param path: The directory path.
        :param index: The index of the file.
        :return: Nothing
        """
        with open(path + f'data\\{index}.txt', 'w', encoding='utf-8') as f:
            for sentence in self.sentences_article:
                f.write(sentence + '\n')
            print(f'WikipediaReader: The file {index}.txt was saved successfully.')
        with open(path + f'ground_truth\\{index}.gt', 'w', encoding='utf-8') as f:
            for sentence in self.sentences_gt:
                f.write(sentence + '\n')
            print(f'WikipediaReader: The file {index}.gt was saved successfully.')

    @staticmethod
    def __validation(gt, sentences_article):
        """
        This method takes as input the sentences of the article and check that all the sentences of the article are
        inside the gt vector. This also checks that all sentences in gt vector are inside the sentences article.
        For the sentences article we must remove the $ starting symbol if it is there, because the sentences in gt have
        not the $ symbol in the first place. Also, there are sentences in gt that have the following format '% [x]',
        where x is a number and those sentences must be ignored.
        :param gt: Ground truth sentences.
        :param sentences_article: Test sentences data.
        :return: True if valid, false if not.
        """
        # Remove the $ symbol if it is there:
        sentences_article = [art[1:] if art[0] == '$' else art for art in sentences_article]
        # Remove the sentences with the format '% [x]'
        gt = [art for art in gt if art[0] != '%']
        # Check that all sentences in gt are in sentences_article:
        for art in gt:
            if art not in sentences_article:
                print(f'WikipediaReader: The sentence {art} is not in the sentences article.')
                return False
        # Check that all sentences in sentences_article are in gt:
        for art in sentences_article:
            if art not in gt:
                print(f'WikipediaReader: The sentence {art} is not in the gt.')
                return False
        return True

    def __split_into_sentences_only(self, article: list) -> list:
        """
        This method does the same as __split_into_sentences_and_add but without the temporal jumps.
        :param article: The article to split.
        :return: The sentences of the article.
        """
        sentences_article = list()
        for counter, art in enumerate(article):
            split_art = art.split('. ')[0:2 * self.max_block_len]
            extend_split = [split for split in split_art if split != '']
            new_split_art = list()
            for i, _art in enumerate(extend_split):
                if _art[0].islower():
                    new_split_art[-1] += '. ' + _art
                elif i > 1:
                    if extend_split[i - 1][-1].isupper():
                        new_split_art[-1] += '. ' + _art
                    else:
                        new_split_art.append(_art)
                else:
                    new_split_art.append(_art)
            extend_split = new_split_art
            # Remove the fist space if exists:
            if extend_split[0][0] == ' ':
                extend_split[0] = extend_split[0][1:]
            sentences_article.extend(extend_split)
            sentences_article.append(f'% {counter}')
        return sentences_article

    def __read_article(self, number_of_articles: int) -> list:
        """
        This method reads the article from Wikipedia.
        :param number_of_articles: The number of articles to read. [articles]
        :return: A list with the articles.
        """
        error_counter = 0
        article = list()
        while len(article) < number_of_articles:
            try:
                self.__soup = self.__get_soup()
                article.append(self.__parse_article(self.__get_article()))
                error_counter = 0
            except Exception as ex:
                print(f'WikipediaReader: {ex}')
                error_counter += 1
                if error_counter > 5:
                    print('WikipediaReader: Too many errors. Exiting...')
                    raise ex
        return article

    def __split_into_sentences_and_add(self, article: list) -> tuple[list, list]:
        """
        This method splits the article into sentences.
        1. Add $ randomly at the beginning of the articles.
        2. Get the residual part and the max part.

        :param article: A list with the articles.
        :return: A list with the sentences of the article.
        """
        sentences_article = list()
        residual = list()
        for art in article:
            # Add the temporal jump if the random number is less than the probability of detection:
            if np.random.rand() < self.prob_true_detection:
                art = '$' + art
            split_art = art.split('. ')[:self.max_block_len]
            # Residual part of the topic over max_block_len
            _res = art.split('. ')[self.max_block_len:]
            if _res:
                to_extend_sentences = [__res for __res in _res if __res != ''][:self.max_block_len]
                for index, to_extend in enumerate(to_extend_sentences):
                    if index == 0:
                        if np.random.rand() < self.prob_true_detection:
                            to_extend_sentences[index] = '$' + to_extend
                    else:
                        if np.random.rand() < self.prob_fake_detection:
                            to_extend_sentences[index] = '$' + to_extend
            else:
                to_extend_sentences = []
            # Append the item in the list "split_art" to the previous element if it starts with lower case:
            extend_split = [split for split in split_art if split != '']
            if extend_split[0][1] == ' ' and extend_split[0][0] == '$':
                extend_split[0] = '$' + extend_split[0][2:]
            new_split_art = list()
            for i, _art in enumerate(extend_split):
                if _art[0].islower():
                    new_split_art[-1] += '. ' + _art
                elif i > 1:
                    if extend_split[i - 1][-1].isupper():
                        new_split_art[-1] += '. ' + _art
                    else:
                        new_split_art.append(_art)
                else:
                    new_split_art.append(_art)
            extend_split = new_split_art
            # The same for residual.
            new_split_art = list()
            for i, _art in enumerate(to_extend_sentences):
                if _art[0].islower():
                    new_split_art[-1] += '. ' + _art
                elif i > 1:
                    if to_extend_sentences[i - 1][-1].isupper():
                        new_split_art[-1] += '. ' + _art
                    else:
                        new_split_art.append(_art)
                else:
                    new_split_art.append(_art)
            to_extend_sentences = new_split_art
            # Add the temporal jump if the random number is less than the probability of false detection:
            for index, split in enumerate(extend_split):
                if split != "":
                    if np.random.rand() < self.prob_fake_detection:
                        extend_split[index] = ('$' + split).replace('$$', '$')
            # Remove the fist space if exists:
            if extend_split[0][0] == ' ':
                extend_split[0] = extend_split[0][1:]
            sentences_article.extend(extend_split)
            residual.extend(to_extend_sentences)
        return sentences_article, residual

    def __get_soup(self) -> BeautifulSoup:
        """
        This method returns the soup of the article.
        :return: A BeautifulSoup object.
        """
        response = requests.get(self.url)
        soup = BeautifulSoup(response.text, 'html.parser')
        return soup

    def __get_article(self) -> str:
        """
        This method returns the body of the article as a string.
        :return: A string with the body of the article.
        """
        article = self.__soup.find(id='mw-content-text')
        article = article.find_all(['p'])
        article = [str(p) for p in article]
        article = ' '.join(article)
        return article

    @staticmethod
    def __parse_article(article: str) -> str:
        """
        This method parses the article and returns the parsed article. The article is parsed obtaining the text of the
        HTML body returned by the __get_article() method.

        Additionally, this method removes the references from the article and removes the invalid characters not
        compatible with utf-8.
        Additionally, this method removes all expressions with the following format: [x] where x anything.

        :param article: A string with the HTML body of the article.
        :return: The parsed article.
        """
        article = BeautifulSoup(article, 'html.parser')
        # Remove the references
        for ref in article.find_all('sup', {'class': 'reference'}):
            ref.decompose()
        # Remove the invalid characters
        article = article.get_text().replace('\xa0', ' ')
        # Remove the invalid characters
        article = article.replace('\t', ' ')
        # Remove the invalid characters
        article = article.replace('\n', ' ')
        # Remove the invalid characters
        article = article.replace('\r', ' ')
        # Remove the invalid characters
        article = article.replace('\f', ' ')
        # Remove the invalid characters
        article = article.replace('\v', ' ')
        # Remove the invalid characters
        article = article.replace('\u200e', ' ')
        # Remove the invalid characters
        article = article.replace('\u200f', ' ')
        # Remove the invalid characters
        article = article.replace('\u202a', ' ')
        # Remove the invalid characters
        article = article.replace('\u202c', ' ')
        # Remove the invalid characters
        article = article.replace('\u202d', ' ')
        # Remove the invalid characters
        article = article.replace('\u202e', ' ')
        # Remove the invalid characters
        article = article.replace('\u200b', ' ')
        # Remove the invalid characters
        article = article.replace('\u200c', ' ')
        # Remove the invalid characters
        article = article.replace('\u200d', ' ')
        # Remove the invalid characters
        article = article.replace('\u2060', ' ')
        # Remove the invalid characters
        article = article.replace('\u2061', ' ')
        # Remove the invalid characters
        article = article.replace('\u2062', ' ')
        # Remove the invalid characters
        article = article.replace('\u2063', ' ')
        # Remove the invalid characters
        article = article.replace('\u2064', ' ')
        # Remove the invalid characters
        article = article.replace('\u2066', ' ')
        # Remove the invalid characters
        article = article.replace('\u2067', ' ')
        # Remove the invalid characters
        article = article.replace('\u2068', ' ')
        # Remove the invalid characters
        article = article.replace('\u2069', ' ')
        # Remove the invalid characters
        article = article.replace('\u2028', ' ')
        # Remove the invalid characters
        article = article.replace('×', ' ')
        # Remove the invalid characters
        article = article.replace('÷', ' ')
        # Remove the invalid characters
        article = article.replace('•', ' ')
        # Remove the invalid characters
        article = article.replace('‣', ' ')
        # Remove the invalid characters
        article = article.replace('O﻿', ' ')
        # Remove the invalid characters
        article = article.replace('﻿', ' ')
        # Remove the invalid characters
        article = article.replace('﻿', ' ')
        # Remove the double or more spaces
        article = article.replace('    ', ' ')
        article = article.replace('   ', ' ')
        article = article.replace('   ', ' ')
        article = article.replace('  ', ' ')
        return article

    @staticmethod
    def __filter_by_number_of_words(articles: list[str], number_of_words: int = 50) -> list:
        """
        This method filters the article by the number of words, and returns a list with the articles that satisfies that
        the number of weords is less or equal to the number_of_words parameter.
        :param articles: List of articles.
        :param number_of_words: The number of words to filter the articles. [words]
        :return: A list with the articles that satisfies that the number of weords is less or equal to
         the number_of_words
        """
        true_articles = list()
        for article in articles:
            if len(article.split(' ')) <= number_of_words:
                true_articles.append(article)
        return true_articles
# - x - x - x - x - x - x - x - x - x - x - x - x - x - x - #
#                        END OF FILE                        #
# - x - x - x - x - x - x - x - x - x - x - x - x - x - x - #
