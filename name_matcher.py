import numpy as np

# globals - the IPA symlist and the symlist to matrix index


symlist = ['^','a:','@','..','e','e:(r)','i','i:','o','o:','u','u:','ai','au','Ou','e..(r)','ei','i..(r)','oi','u..(r)','b','d','f','g','h','j','k','l','m','n','N','p','r','s','S','t','tS','th','TH','v','w','z','Z','dZ']

p2n = {symlist[i]:i for i in range(len(symlist))}

class NameMatcher:
    '''
    NameMatcher is a class used to compare two strings using sequence matching.
    The best possible score is returned using certain criteria based on a scoring matrix and gap penalties.
    '''
    def __init__(self, matrix_location, gap_penalty):
        '''
        __init__(matrix_location, gap_penalty)
        This method sets up the NameMatcher.
        matrix_location - the file location of the scoring matrix. 
        The scoring matrix is a 44x44 symmetric matrix containing the similarity between any two alphabets from the IPA. The similarity is a number between [0,1]
        The order of the row/colomn headings is the same as that in the global symlist.
        It's a comma separated file with a row per line.
        gap penalty - the score subtracted for each gap in the alignment. Typical values are [0,1]
        '''
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
        match(s1,s2) -> best match score
        Finds and returns best possible match score between s1 and s2
        s1 = [] where s1 contains elements of symlist only
        s2 = [] where s2 contains elements of symlist only
        '''
        align_mat = np.ones((len(s1), len(s2))) * -500
        return self._S(len(s1)-1, len(s2)-1, align_mat, s1, s2)


    def _S(self,i,j,mat, s1, s2):
        '''
        _S(i,j,mat,s1,s2) -> S(i,j)
        S(i,j) := maximum sum till (i,j)
        This is the internal workhorse function to fill the s1*s2 matrix with the maximum sums.

        This is almost a direct implementation of the following, where score is the value in the scoring matrix corresponding to the ith IPA of the string s1 and the jth IPA of the string s2.

        S(i,j) = max{
                      S(i-1, j-1) + score(i,j)
                      x>=1 max{ S(i-x, j) - x*gap_penalty}
                      y>=1 max{ S(i, j-y) - y*gap_penalty}
                    }
        '''

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
    '''
    name_matcher_test()
    Method to test the NameMatcher
    '''
    nm = NameMatcher('comparison_matrix', 0.15)
    print(nm.match(['d','Ou', 'g'], ['tS','@', 't', 'au']))


# name_matcher_test()
