class linguistic_distance(object):
    '''
    This class calculates the Levenshtein distance between two words.
    '''

    def __init__(self):
        pass


    def levenshtein(self, s1, s2):
        '''
        Calculates Levenshtein distance between two words. Instead of populating a matrix, we continually update a list
        that represents one row of the matrix. The final entry of the final list is taken as the distance between words.
        :param s1: first string
        :param s2: second string
        :return: Levenshtein distance
        '''
        # check to make sure we are using the longer word as our main list, to avoid early termination
        if len(s1) > len(s2):
            s1, s2 = s2, s1

        dist1 = range(len(s1) + 1) # initialize first row
        for i2, c2 in enumerate(s2):
            dist2 = [i2 + 1] # initialize first entry of next row
            for i1, c1 in enumerate(s1):
                if c1 == c2:
                    dist2.append(dist1[i1])
                else:
                    dist2.append(1 + min((dist1[i1], dist1[i1 + 1], dist2[-1])))
            dist1 = dist2
        return dist1[-1]