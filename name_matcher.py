'''
Given two names, this returns best possible score for the matching using the matrix
'''
import numpy as np

class NameMatcher:
    def __init__(self, matrix_location, gap_penalty):
        f = open(matrix_location)
        self.mat = []
        for line in f:
            r = []
            for elem in line[:-1].split(','):
                r.append(float(elem.strip()))
            self.mat.append(r)
        f.close()
        self.mat = np.mat(self.mat)
        self.delta = gap_penalty



def name_matcher_test():
    nm = NameMatcher('comparison_matrix', 15)
    print(nm.mat)
    print(nm.delta)


name_matcher_test()
