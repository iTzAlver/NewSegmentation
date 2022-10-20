# -------------------------------------------------------------------#
#                                                                    #
#    Author:    Alberto Palomo Alonso.                               #
#                                                                    #
#    Git user:  https://github.com/iTzAlver                          #
#    Email:     ialver.p@gmail.com                                   #
#                                                                    #
# -------------------------------------------------------------------#
import numpy as np
from ._structures import TreeStructure


# -------------------------------------------------------------------#
#   x   x   x   x   x   x   x   x   x   x   x   x   x   x   x   x    #
# -------------------------------------------------------------------#
def save3s(object_array, path):
    with open(f'{path}.3s', "w", encoding='utf-8') as myfile:
        for tree in object_array:
            myfile.writelines('{' + '\n')
            myfile.writelines('\tRef:' + str(tree.Reference) + '\n')
            myfile.writelines('\tID:' + str(tree.ID) + '\n')
            myfile.writelines('\tCP:' + str(tree.CP) + '\n')
            myfile.writelines('\tTime:' + str(tree.Time) + '\n')
            myfile.writelines('\tPayload:' + str(tree.Payload) + '\n')
            myfile.writelines('\tCode:' + str(tree.Embedding) + '\n')
            for leaf in tree:
                myfile.writelines('\t\t' + str(leaf.ID) + '\n')
                myfile.writelines('\t\t' + str(tree.Payload) + '\n')
                myfile.writelines('\t\t' + str(tree.Embedding) + '\n')
            myfile.writelines('\tCode:' + str(tree.Embedding) + '\n')
            myfile.writelines('}' + '\n')
            myfile.writelines('\n')
    return myfile


def load3s(path):
    the_trees = []
    if not len(path) > 0:
        print('Invalid path file for loading trees...')
        return []
    if path[-3:] != '.3s':
        thepath = f'{path}.3s'
    else:
        thepath = path
    with open(thepath, "r", encoding='utf-8') as myfile:
        a_tree = TreeStructure()
        for line in myfile:
            if line[0] == '{':
                a_tree = TreeStructure()
            elif line[0] == '\t':
                if line[1] == '\t':
                    largs = [0, '', []]
                    largs[0] = int(line[2:len(line) - 1])
                    line = next(myfile)
                    largs[1] = line[2:len(line)-1]
                    line = next(myfile)
                    largs[2] = _readcode(line, myfile, posex=3)
                    a_tree.add(Leaf=tuple(largs))
                elif line[1:5] == 'Ref:':
                    rest = int(line[5:])
                    a_tree.add(ref=rest)
                elif line[1:4] == 'ID:':
                    rest = int(line[4:])
                    a_tree.add(ID=rest)
                elif line[1:4] == 'CP:':
                    rest = float(line[4:])
                    a_tree.add(CP=rest)
                elif line[1:9] == 'Payload:':
                    rest = line[9:]
                    a_tree.add(Payload=rest)
                elif line[1:6] == 'Time:':
                    rest = float(line[6:])
                    a_tree.add(Time=rest)
                elif line[1:6] == 'Code:':
                    a_tree.add(Code=_readcode(line, myfile))

            elif line[0] == '}':
                the_trees.append(a_tree)
    return the_trees


def _readcode(line, file, posex=7):
    rest = list()
    rest.append(line[posex:].strip('\n'))
    while rest[-1][-1] != ']':
        line = next(file)
        rest.append(line[1:].strip('\n'))
    rest[-1] = rest[-1].strip(']')
    unirest = ' '.join(rest)
    unirest = unirest.split(' ')
    codex = []
    for item in unirest:
        if item:
            codex.append(float(item))
    return np.array(codex)
# -------------------------------------------------------------------#
#           E   N   D          O   F           F   I   L   E         #
# -------------------------------------------------------------------#
