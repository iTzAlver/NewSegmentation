# - x - x - x - x - x - x - x - x - x - x - x - x - x - x - #
#                                                           #
#   This file was created by: Alberto Palomo Alonso         #
# Universidad de Alcalá - Escuela Politécnica Superior      #
#                                                           #
# - x - x - x - x - x - x - x - x - x - x - x - x - x - x - #
# Import statements:
import json
import os
from abc import abstractmethod

import matplotlib.pyplot as plt
import numpy as np
from nltk.metrics.segmentation import windowdiff, pk
from sklearn.metrics.pairwise import cosine_similarity

from ._dserial import save3s
from ._gtreader import gtreader
from ._structures import TreeStructure
from ._tdm import ftdm

temporalfile = r'./temporalfile.txt'


# -----------------------------------------------------------
class NewsSegmentation:
    def __init__(self, news_path: str,
                 tdm: float = 0.245,
                 gpa: tuple = (0, 0),
                 sdm: tuple = (0.177, 1, 0.177*0.87),
                 lcm: tuple = (0.614,),
                 ref: int = 0,
                 cache_file: str = '',
                 dump: bool = True):
        """
        Virtual class: 3 methods must be overriden
        :param tdm: Penalty factor (betta) for Temporal Distance Manager
        :param sdm: Spatial Distance Manager parameters:
            [0]: [0]: Variance for Gaussian.
                 [1]: Weight for GPA.
            [1]: SDM algorithm parameters.
        :param lcm: Algorithm parameters for Later Correlation Manager.
        """
        # Parameters for each module of the architecture.
        self.parameters = {"betta_tdm": tdm, "gpa": gpa, "sdm": sdm, "lcm": lcm}
        self.reference = ref
        # Attribute initialization.
        self.News = []
        self.R = []
        self.s = []
        self.t = []
        self.p = []
        # Private parameters.
        self._efficientembedding = []
        self._initial_efficientembedding = []
        self._directives = []
        self._cache = {}
        self._cache_file = cache_file
        # Loading cache file if exists:
        if self._cache_file:
            if self._cache_file.split('.')[-1] != 'json':
                self._cache_file = f'{cache_file}.json'
            if os.path.exists(self._cache_file):
                try:
                    with open(self._cache_file, 'r', encoding='utf-8') as file:
                        _cache = json.load(file)
                        for key, item in _cache.items():
                            self._cache[key] = np.array(item)
                except Exception as ex:
                    print(ex)
                    self._cache_file = False
        # Steps for in the architecture.
        if '.txt' in news_path:
            news_path_txt = news_path
        else:
            news_path_txt = self.__database_transformation(news_path)

        p, s, t = self.__reader(news_path_txt)
        self.p = p
        self.s.append(s)
        self.t.append(t)

        _r, r, s, t = self.__temporal_manager(p, s, t)
        self.R.append(_r)
        self.R.append(r)
        self.s.append(s)
        self.t.append(t)
        self._initial_efficientembedding = self._efficientembedding.copy()

        r, s, t = self.__spatial_manager(r, s, t)
        self.R.append(r)
        self.s.append(s)
        self.t.append(t)

        r, s, t = self.__later_correlation_manager(s, t)
        self.R.append(r)
        self.s.append(s)
        self.t.append(t)
        # Tree transformation:
        self.__treefication()
        self.performance = {}
        self.NewsReference = None

        if dump and self._cache_file:
            self._dump_cache()

        if os.path.exists(temporalfile):
            os.remove(temporalfile)

    def __database_transformation(self, path: str):
        return self._database_transformation(path, temporalfile)

    @staticmethod
    def __reader(path: str):
        s = []
        p = []
        t = []
        linenumber = 0
        with open(path, 'r', encoding='utf-8') as file:
            for _line in file:
                if _line[0] == '%':
                    _str_t = _line[2:-1].split(', ')
                    t = np.array([float(str_t) for str_t in _str_t])
                else:
                    if _line[0] == '$':
                        p.append(linenumber)
                        line = _line[1:]
                    else:
                        line = _line
                    s.append(line.strip('\n'))
                linenumber += 1

        for index, sentence in enumerate(s):
            if sentence[-1] == ' ':
                s[index] = sentence[:-1]
            if sentence[0] == ' ':
                s[index] = sentence[1:]
        return p, s, t

    def __specific_language_model(self, s: list[str]) -> np.array:
        # Check the cache.
        sx = []
        for sentence in s:
            if sentence not in self._cache:
                sx.append(sentence)
        # Get the embeddings.
        embeddings_ = self._specific_language_model(sx)
        # Store the embeddings in cache.
        for place, sentence in enumerate(sx):
            self._cache[sentence] = embeddings_[place]

        # Restore the embeddings.
        embeddings = []
        for sentence in s:
            embeddings.append(self._cache[sentence])
        embeddings = np.array(embeddings)
        # Get correlation values.
        r = np.zeros((len(s), len(s)))
        for ne1, embedding1 in enumerate(embeddings):
            for ne2, embedding2 in enumerate(embeddings):
                value = cosine_similarity(embedding1.reshape(1, -1), embedding2.reshape(1, -1))[0][0]
                r[ne1][ne2] = value
                r[ne2][ne1] = value
        self._efficientembedding = embeddings
        return r

    def __temporal_manager(self, p: (list[int], np.ndarray), s: list[str], t: (list[float], np.ndarray)) -> tuple:
        r0, r1 = ftdm(p, s, self.__specific_language_model, self.parameters["betta_tdm"])
        return r0, r1, s, t

    def __spatial_manager(self, r: np.ndarray, s: list[str], t: (list[float], np.ndarray)):
        # GPA sub-module:
        rp = np.zeros((len(r), len(r)))
        for nr, row in enumerate(r):
            for nc, element in enumerate(row):
                # ['gpa'][0] -> Variance for Gaussian.
                # ['gpa'][1] -> w for Gaussian.
                gpa = np.exp(-((nr - nc) ** 2) / (2 * self.parameters['gpa'][0])) \
                    if self.parameters['gpa'][0] > 0 else element
                rp[nr][nc] = element + self.parameters['gpa'][1] * (gpa - element)
        # SDM algorithm:
        self._directives = self._spatial_manager(rp, self.parameters['sdm'])
        if not self._directives:
            self._directives = list(range(1, len(rp)))
        # Merge components:
        s2 = []
        t2 = []
        _s = ''
        _t = 0
        for pos, phrase in enumerate(s):
            if pos in self._directives:
                s2.append(_s)
                t2.append(_t)
                _s = f'{phrase}'
                _t = 0
                _t += t[pos]
            else:
                _s = f'{_s}. {phrase}'
                _t += t[pos]
        s2.append(_s)
        t2.append(_t)
        s2[0] = s2[0][2:]
        return rp, s2, np.array(t2)

    def __later_correlation_manager(self, s: list[str], t: (list[float], np.ndarray)):
        r, s, t = self._later_correlation_manager(self.__specific_language_model, s, t, self.parameters['lcm'])
        return np.array(r), s, np.array(t)

    def __treefication(self):
        initial_s = self.s[0]
        end_s = self.s[-1]
        tinfo = self.t[-1]
        for treeid, payload in enumerate(end_s):
            leafs = []
            cembedding = []
            for leaf_id, initial in enumerate(initial_s):
                if initial in payload:
                    leafs.append((leaf_id, initial, self._initial_efficientembedding[leaf_id]))
                    cembedding.append(self._initial_efficientembedding[leaf_id])
            tree = TreeStructure(*tuple(leafs), ID=treeid, embedding=self._efficientembedding[treeid], payload=payload,
                                 time=tinfo[treeid], reference=self.reference, CP=self.__cpcalc(cembedding))
            self.News.append(tree)

    @staticmethod
    def __cpcalc(cembedding: (list, np.ndarray)):
        r = np.zeros((len(cembedding), len(cembedding)))
        for ne1, emb1 in enumerate(cembedding):
            for ne2, emb2 in enumerate(cembedding):
                value = cosine_similarity(emb1.reshape(1, -1), emb2.reshape(1, -1))[0][0]
                r[ne1][ne2] = value
                r[ne2][ne1] = value
        cp = 0
        for nr, row in enumerate(r):
            for nc, element in enumerate(row):
                if nc > nr:
                    cp += element ** 2
        cp /= len(cembedding) * (len(cembedding) - 1) if len(cembedding) > 1 else 1
        return np.float(2 * cp)

    @staticmethod
    @abstractmethod
    def _spatial_manager(r: np.ndarray, param: tuple) -> tuple:
        pass

    @staticmethod
    @abstractmethod
    def _later_correlation_manager(lm: any, s: list[str], t: (list[float], np.ndarray), param: tuple) -> tuple:
        pass

    @staticmethod
    @abstractmethod
    def _specific_language_model(s: list[str]) -> np.array:
        pass

    @staticmethod
    @abstractmethod
    def _database_transformation(path: str, output: str):
        pass

    def __repr__(self):
        __text = f"NewsSegmentation object: {len(self.News)} news classified."
        return __text

    def __iter__(self):
        self.__n = 0
        return self

    def __next__(self):
        while self.__n < len(self.News):
            rval = self.News[self.__n]
            self.__n += 1
            return rval
        else:
            raise StopIteration

    def __len__(self):
        return len(self.News)

    def __bool__(self):
        for news in self.News:
            if not news.isValid:
                return False
        return True

    def __add__(self, other):
        if isinstance(other, TreeStructure):
            if other.isValid:
                self.News.append(other)

    def plotmtx(self, *args, color='orange'):
        if color not in ['orange', 'black']:
            print(f'Warning: Color: {color} not defined. Orange chosen.')
            color = 'orange'
        if len(args) == 0:
            args_ = (0, 1, 2, 3)
        else:
            args_ = args
        marks = len(args_)
        _, subfigs = plt.subplots(ncols=marks)
        for nfig, num in enumerate(args_):
            num = 3 if num > 3 else num
            pltmtx = self.R[num]
            thematrix = np.zeros((len(pltmtx), len(pltmtx), 3), dtype=np.uint8)
            nra = 100 if color == 'orange' else 255
            wxf = 1 if num == 3 else 0
            wxp = 1 if num == 2 else 0
            wxb = 0 if color == 'orange' else 255
            bluecore = 150 if color == 'orange' else -150
            for nrow, row in enumerate(pltmtx):
                xrow = row.copy()
                if len(xrow) > 1:
                    mrow = (xrow.sort(), xrow[-2])[1]
                else:
                    mrow = None
                for ncol, element in enumerate(row):
                    thematrix[nrow][ncol][0] = [element * 255 if element > 0 else 0][0]
                    thematrix[nrow][ncol][1] = [element * nra if element > 0 else 0][0]
                    thematrix[nrow][ncol][2] = [element * wxb if element > 0 else 0][0]
                    if element == mrow and wxf:
                        thematrix[nrow][ncol][2] += 100
            if wxp:
                thesegmentation = [0]
                thesegmentation.extend(self._directives)
                for idx, segment in enumerate(self._directives):
                    base = thesegmentation[idx]
                    ending = segment - 1
                    for index1 in range(ending - base + 1):
                        for index2 in range(ending - base + 1):
                            thematrix[base + index2][base + index1][2] += bluecore
            subfigs[nfig].imshow(thematrix)
            subfigs[nfig].set_title(f'R{num}')
        plt.show()
        return self

    @staticmethod
    def _whereis(sentence: str, trees: list[TreeStructure]):
        for tree in trees:
            if sentence in tree.Payload:
                return tree.ID
        raise ZeroDivisionError(f'Sentence "{sentence}" not in tree, something is working wrong...')

    def whereis(self, sentence: str):
        if self.News:
            for tree in self.News:
                if sentence in tree.Payload:
                    return tree.ID
            raise None
        else:
            raise ValueError('Error while searching a sentence in the trees. Trees are not valid, try rebuilding '
                             'the object again.')

    def evaluate(self, reference_trees_: (list[TreeStructure], str), show: bool = False, integrity_check: bool = True):
        # Initial checks:
        if isinstance(reference_trees_, str):
            reference_trees = gtreader(reference_trees_)
        elif isinstance(reference_trees_, list):
            reference_trees = reference_trees_
        else:
            raise ValueError('Argument must be a list of trees or path to a GT file.')

        if integrity_check:
            pl1 = self.s[0]
            pl2 = []
            for tree in reference_trees:
                for leaf in tree:
                    pl2.append(leaf.Payload)

            for sentence in pl1:
                if sentence not in pl2:
                    raise ValueError(f'Integrity validation for evaluation failed:\nOriginal sentence: '
                                     f'"{sentence}" not in reference tree.')
            for sentence in pl2:
                if sentence not in pl1:
                    raise ValueError(f'Integrity validation for evaluation failed:\nReference sentence: '
                                     f'"{sentence}" not in original sentences.')

        # Evaluation:
        results = {'Precision': 0, 'Recall': 0, 'F1': 0, 'WD': 0}
        trees = self.News
        confusion_matrix = np.zeros((len(reference_trees), len(trees)))
        for ngt, gt in enumerate(reference_trees):
            for ntr, tree in enumerate(trees):
                for leaf in tree:
                    confusion_matrix[ngt][ntr] += len(leaf.Payload.split(' ')) if leaf.Payload in gt.Payload else 0

        pertenence = []
        tp = 0
        fp = 0
        for row in np.transpose(confusion_matrix):
            indexmax = np.argmax(row)
            pertenence.append(indexmax)
            tp += max(row)
            fp += sum(row) - max(row)

        fn = sum([sum(col) - max(col) for col in confusion_matrix])

        results['Precision'] = tp / (tp + fp)
        results['Recall'] = tp / (tp + fn)
        results['F1'] = 2 * results['Precision'] * results['Recall'] / (results['Precision'] + results['Recall'])

        s_res = []
        s_ref = []
        for _ in self.s[0]:
            s_res.append(0)
            s_ref.append(0)

        original = self.s[0]
        last_ref = 0
        last_res = 0
        for index, sentence in enumerate(original):
            ntree_res = self._whereis(sentence, self.News)
            ntree_ref = self._whereis(sentence, reference_trees)
            if ntree_res != last_res:
                last_res = ntree_res
                s_res[index] = 1
            if ntree_ref != last_ref:
                last_ref = ntree_ref
                s_ref[index] = 1

        s_res_s = ''
        for item in s_res:
            if item:
                s_res_s = f'{s_res_s}1'
            else:
                s_res_s = f'{s_res_s}0'
        s_ref_s = ''
        for item in s_ref:
            if item:
                s_ref_s = f'{s_ref_s}1'
            else:
                s_ref_s = f'{s_ref_s}0'

        k = round(0.5 * len(s_res) / (1 + sum(s_ref)))
        results['WD'] = windowdiff(s_ref_s, s_res_s, k)
        results['Pk'] = pk(s_ref_s, s_res_s, k)

        if show:
            # _, subfigs = plt.subplots(ncols=2, nrows=2)
            fig = plt.figure()
            gs = fig.add_gridspec(6, 2)
            subfigs = list()
            subfigs.append(fig.add_subplot(gs[0:2, 0]))
            subfigs.append(fig.add_subplot(gs[0:2, 1]))
            subfigs.append(fig.add_subplot(gs[3, 0:2]))
            subfigs.append(fig.add_subplot(gs[5:7, 0:2]))

            pltmtx = self.R[2]
            thematrix = np.zeros((len(pltmtx), len(pltmtx), 3), dtype=np.uint8)
            for nrow, row in enumerate(pltmtx):
                for ncol, element in enumerate(row):
                    thematrix[nrow][ncol][0] = [element * 255 if element > 0 else 0][0]
                    thematrix[nrow][ncol][1] = [element * 100 if element > 0 else 0][0]
                    thematrix[nrow][ncol][2] = [element * 000 if element > 0 else 0][0]
            thematrix2 = thematrix.copy()
            thesegmentation = [0]
            thesegmentation.extend(self._directives)

            for idx, segment in enumerate(self._directives):
                base = thesegmentation[idx]
                ending = segment - 1
                for index1 in range(ending - base + 1):
                    for index2 in range(ending - base + 1):
                        thematrix[base + index2][base + index1][2] += 150

            subfigs[0].imshow(thematrix)
            subfigs[0].set_title(f'Performed segmentation.')
            subfigs[0].set_xlabel('Sentence index')
            subfigs[0].set_ylabel('Sentence index')

            thesegmentation = [0]
            _directives = []
            for index, element in enumerate(s_ref):
                if element:
                    _directives.append(index)
            _directives.append(len(s_ref))
            thesegmentation.extend(_directives)
            for idx, segment in enumerate(_directives):
                base = thesegmentation[idx]
                ending = segment - 1
                for index1 in range(ending - base + 1):
                    for index2 in range(ending - base + 1):
                        thematrix2[base + index2][base + index1][2] += 150
            subfigs[1].imshow(thematrix2)
            subfigs[1].set_title(f'Correct segmentation.')
            subfigs[1].set_xlabel('Sentence index')
            subfigs[1].set_ylabel('Sentence index')

            mtwd = np.zeros((2, len(s_res), 3), dtype=np.uint8)
            for i in range(3):
                mtwd[0, :, i] = 255 * np.array(s_res)
                mtwd[1, :, i] = 255 * np.array(s_ref)
            subfigs[2].imshow(mtwd)
            subfigs[2].set_title('Segmentation boundaries.')
            subfigs[2].set_xlabel('Sentence index')
            subfigs[2].set_yticks(np.array([0, 1]), labels=['Reference', 'Performed'])

            mtreep = np.zeros((max(len(self.News), len(reference_trees)), len(original), 3), dtype=np.uint8)
            for ns, sentence in enumerate(original):
                for tree in self.News:
                    if sentence in tree.Payload:
                        mtreep[tree.ID, ns, 0] = 255

                for tree in reference_trees:
                    if sentence in tree.Payload:
                        mtreep[tree.ID, ns, 2] = 255

            subfigs[3].imshow(mtreep)
            subfigs[3].set_title('Sentence pertenence.')
            subfigs[3].set_xlabel('Sentence index')
            subfigs[3].set_ylabel('Tree ID')
            plt.show()
        self.performance = results
        self.NewsReference = reference_trees
        return results

    @staticmethod
    def info():
        __text = 'News segmentation package:\n--------------------------------------------\nFAST USAGE:\n' \
                 '--------------------------------------------\nPATH_TO_MY_FILE = < PAHT >\n' \
                 'import newsegmentation as ns\nnews = ns.NewsSegmentation(PATH_TO_MY_FILE)\n' \
                 'for pon in news:\n' \
                 '\tprint(pon)\n' \
                 '--------------------------------------------\n'
        print(__text)
        return __text

    @staticmethod
    def about():
        __text = 'Institution:\n------------------------------------------------------\n' \
                 'Universidad de Alcalá.\nEscuela Politécnica Superior.\n' \
                 'Departamento de Teoría De la Señal y Comunicaciones.\nCátedra ISDEFE.\n' \
                 '------------------------------------------------------\n' \
                 'Author: Alberto Palomo Alonso\n' \
                 '------------------------------------------------------\n'
        print(__text)
        return __text

    def save(self, path: str):
        save3s(self.News, path)
        return self

    def _dump_cache(self):
        if self._cache_file:
            try:
                with open(self._cache_file, 'w', encoding='utf-8') as file:
                    _cache = {}
                    for key, item in self._cache.items():
                        _cache[key] = item.tolist()
                    json.dump(_cache, file)
            except Exception as ex:
                print(ex)
# - x - x - x - x - x - x - x - x - x - x - x - x - x - x - #
#                        END OF FILE                        #
# - x - x - x - x - x - x - x - x - x - x - x - x - x - x - #
