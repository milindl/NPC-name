'''
Given two names, this returns best possible score for the matching using the matrix
'''
import numpy as np

# globals!


symlist = ['^','a:','@','..','e','e:(r)','i','i:','o','o:','u','u:','ai','au','Ou','e..(r)','ei','i..(r)','oi','u..(r)','b','d','f','g','h','j','k','l','m','n','N','p','r','s','S','t','tS','th','TH','v','w','z','Z','dZ']

p2n = {symlist[i]:i for i in range(len(symlist))}

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
        self.mat = np.array(self.mat)
        self.delta = gap_penalty

    def match(self, s1, s2):
        '''
        Finds and returns best possible match score between s1 and s2
        '''
        align_mat = np.ones((len(s1), len(s2))) * -500
        return self._S(len(s1)-1, len(s2)-1, align_mat, s1, s2)


    def _S(self,i,j,mat, s1, s2):
        '''
        use the expression
        _S(i,j) = max of
        1. S(i-1,j-1) + score of ij^th matching as per p2n and self.mat
        2. x>=1 max { S(i-x, j) - x*delta }
        3. y>=1 max { S(i, j-y) - y*delta }
        '''
        '''Terminate it in case it already exists'''
        if mat[i,j] != -500:
            return mat[i,j]
        if i==0 and j==0:
            return self.mat[p2n[s1[0]], p2n[s2[0]]]
        
        possible_max = []
        if i != 0 and j != 0:
            score = self.mat[p2n[s1[i]], p2n[s2[j]]]
            possible_max.append(score + self._S(i-1,j-1,mat,s1,s2))

        x_max = []
        for x in range(1,i+1):
            x_max.append(self._S(i-x, j, mat, s1, s2) - x*self.delta)
            
        y_max = []
        for y in range(1,j+1):
            y_max.append(self._S(i, j-y, mat, s1, s2) - y*self.delta)

        if len(x_max)>0:
            possible_max.append(np.max(x_max))
        if len(y_max)>0:
            possible_max.append(np.max(y_max))

        m = max(possible_max)
        mat[i,j] = m
        return m

            
        

    
def name_matcher_test():
    nm = NameMatcher('comparison_matrix', 0.15)
    print(nm.match(['d','Ou', 'g'], ['tS','@', 't', 'au']))


# name_matcher_test()
