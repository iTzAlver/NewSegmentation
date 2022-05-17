# - x - x - x - x - x - x - x - x - x - x - x - x - x - x - #
#                                                           #
#   This file was created by: Alberto Palomo Alonso         #
# Universidad de Alcalá - Escuela Politécnica Superior      #
#                                                           #
# - x - x - x - x - x - x - x - x - x - x - x - x - x - x - #
import numpy as np


class Leaf:
    def __init__(self, *args):
        if len(args) != 2:
            raise ValueError("Error while building a Leaf, wrong number of parameters.")
        if not isinstance(args[0], int):
            raise ValueError("Error while building a Leaf, first argument must be an int.")
        if args[0] < 0:
            raise ValueError("Warning, wrong ID argument while building a Leaf.")
        if not isinstance(args[1], str):
            raise ValueError("Error while building a Leaf, second parameter is not a string.")
        self.ID = args[0]
        self.Payload = args[1]

    def __iter__(self):
        self._scon = False
        return self

    def __next__(self):
        if self._scon:
            raise StopIteration
        else:
            self._scon = True
            return self.ID, self.Payload

    def __repr__(self):
        return self.Payload

    def __eq__(self, other):
        if isinstance(other, Leaf):
            return other.Payload == self.Payload or self.Payload == other.Payload
        else:
            return other == self.Payload or self.Payload == other


class TreeStructure:
    def __init__(self, *args, **kwargs):
        for tuple_ in args:
            if not isinstance(tuple_, tuple):
                raise Exception("Error while building a TreeStructure: arguments must be a group of tuples.")
            if len(tuple_) != 2:
                raise Exception("Error while building a TreeStructure: parameters in tuples must contain 2 "
                                "elements: (ID, Payload)")
        self.Leafs = [Leaf(ID, payload) for ID, payload in args]
        self.ID = None
        self.Payload = None
        self.Embedding = None
        self.Time = None
        self.CP = None
        self.Reference = None
        self.isValid = False
        self.isComplete = False
        self.add(**kwargs)
        self._n = 0
        return

    def add(self, **kwargs):
        for key, item in kwargs.items():
            if 'ID' in key:
                if isinstance(item, int):
                    self.ID = item
                else:
                    raise ValueError(f"Error while building a TreeStructure: invalid {key} parameter.")
            elif 'load' in key:
                if isinstance(item, str):
                    self.Payload = item
                else:
                    raise ValueError(f"Error while building a TreeStructure: invalid {key} parameter.")
            elif 'bed' in key:
                if isinstance(item, (list, tuple, np.ndarray)):
                    self.Embedding = item
                else:
                    raise ValueError(f"Error while building a TreeStructure: invalid {key} parameter.")
            elif 'ime' in key:
                if isinstance(item, float) or isinstance(item, int):
                    self.Time = item
                else:
                    raise ValueError(f"Error while building a TreeStructure: invalid {key} parameter.")
            elif 'CP' in key:
                if isinstance(item, int) or isinstance(item, float):
                    self.CP = item
                else:
                    raise ValueError(f"Error while building a TreeStructure: invalid {key} parameter.")
            elif 'ef' in key:
                if isinstance(item, int):
                    self.Reference = item
                else:
                    raise ValueError(f"Error while building a TreeStructure: invalid {key} parameter.")

        if self.Payload is None:
            self.Payload = ''
            for leaf in self.Leafs:
                for _, payload in leaf:
                    if self.Payload != '':
                        self.Payload = f'{self.Payload} {payload}'
                    else:
                        self.Payload = f'{payload}'

        if self.ID is None or self.Payload == '' or self.Time is None:
            self.isValid = False
        else:
            self.isValid = True
        if self.Embedding is None or self.CP is None:
            self.isComplete = False
        else:
            self.isComplete = True

    def __repr__(self):
        return self.Payload

    def __iter__(self):
        self._n = 0
        if self.isValid:
            return self
        else:
            raise RuntimeError("Error while creating an iterator from TreeStructure: this tree is not valid, "
                               "try to rebuild it properly.")

    def __eq__(self, other):
        return self.Payload in other or other in self.Payload

    def __next__(self) -> Leaf:
        while self._n < len(self.Leafs):
            lf = self.Leafs[self._n]
            self._n += 1
            return lf
        else:
            raise StopIteration
# - x - x - x - x - x - x - x - x - x - x - x - x - x - x - #
#                        END OF FILE                        #
# - x - x - x - x - x - x - x - x - x - x - x - x - x - x - #
