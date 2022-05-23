# -------------------------------------------------------------------#
#                                                                    #
#    Author:    Alberto Palomo Alonso.                               #
#                                                                    #
#    Git user:  https://github.com/iTzAlver                          #
#    Email:     ialver.p@gmail.com                                   #
#                                                                    #
# -------------------------------------------------------------------#
from ._structures import TreeStructure
# -------------------------------------------------------------------#
#   x   x   x   x   x   x   x   x   x   x   x   x   x   x   x   x    #
# -------------------------------------------------------------------#


def gtreader(path) -> list:
	trees = []
	id_ = []
	payload_ = []
	with open(path, 'r', encoding='utf-8') as file:
		for nline, line in enumerate(file):
			if line[0] == '%':
				pl = '. '.join(payload_)
				leafs = [[ids, payload, []] for ids, payload in zip(id_, payload_)]
				trees.append(TreeStructure(*tuple(leafs), payload=pl, ID=len(trees)))
				payload_ = []
				id_ = []
			else:
				id_.append(nline)
				payload_.append(line.strip('\n'))
	return trees
# -------------------------------------------------------------------#
#           E   N   D          O   F           F   I   L   E         #
# -------------------------------------------------------------------#
