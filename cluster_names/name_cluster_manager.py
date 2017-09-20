class name_cluster_manager(object):
    '''
    This class is the manager for the name cluster algorithm. It forms clusters and prints the resulting labels.
    '''


    def __init__(self, argv):
        '''
        Constructor
        '''
        self.names_file = argv[1]
        self.clusters_to_form = int(argv[2])
        self.names = []
        self.labeling = []

        # Call the read_names function right away
        self.read_names(False)


    def read_names(self, clear_names_first):
        '''
        This function reads the names from storage to memory.
        Input: clear_names_first: True if any existing names should be flushed prior to filling self.names.
        Output: none.
        Precondition: self.names_file is a list of names, one per line.
        Postcondition: self.names is a list of names read from self.names_file
        '''
        if clear_names_first:
            self.names = []
        with open(self.names_file) as f:
            for name in f:
                self.names.append(name.strip())


    def cluster_names(self):
        '''
        This function clusters names based on the levenshtein distance between their soundex representations.
        This is done by passing the matrix of distances between names into an agglomerative clustering model.
        Output: cluster labels
        '''
        from sklearn.cluster import AgglomerativeClustering
        from linguistic_distance import linguistic_distance
        from sound import sound
        sound = sound()
        names_sndx = []
        for n in self.names:
            names_sndx.append(sound.get_soundex(n))
        dists = linguistic_distance()
        distmat = []
        for n1 in names_sndx:
            row = []
            for n2 in names_sndx:
                row.append(dists.levenshtein(n1, n2))
            distmat.append(row)
        clust = AgglomerativeClustering(n_clusters=self.clusters_to_form)
        clust.fit(distmat)
        self.labeling = clust.labels_
        return clust.labels_


    def print_names(self):
        '''
        This function prints the clusters formed in sequential order.
        '''
        import numpy as np
        for i in range(self.clusters_to_form):
            indices = np.where(np.array(self.labeling)==i)
            print ' '.join(np.array(self.names)[indices])
