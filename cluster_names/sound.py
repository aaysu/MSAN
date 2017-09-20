class sound(object):
    '''
    This class converts words into their soundex representations.
    '''


    def __init__(self):
        self.mapping = {
            'B':'1', 'F':'1', 'P':'1', 'V':'1',
            'C':'2', 'G':'2', 'J':'2', 'K':'2', 'Q':'2', 'S':'2', 'X':'2', 'Z':'2',
            'D':'3', 'T':'3',
            'L':'4',
            'M':'5', 'N':'5',
            'R':'6'
        }


    def get_soundex(self, word):
        output = word[0].upper()
        i = 1
        for w in word[1:]:
            val = self.mapping.get(w.upper())
            if val is not None and val != output[-1]:
                output += val
            if len(output) == 4:
                break
            i += 1
        while len(output) < 4:
            output += '0'
        return output
