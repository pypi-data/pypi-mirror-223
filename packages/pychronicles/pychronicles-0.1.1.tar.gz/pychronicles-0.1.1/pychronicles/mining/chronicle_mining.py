#!/bin/python3
# -*- coding: utf-8 -*-
"""
Mining frequent sequences 

@author: Thomas Guyet
@date: 01/2023
@institution: Inria

TODO
    - additional test for episode mining (assess the minimal occurrence)
"""

from pychronicles import Chronicle
from pychronicles import TimedSequence

from typing import Sequence, Union

import numpy as np


class ChronicleMiner:
    """
    Class for frequent chronicle mining from a collection of `TimedSequence`
    """
    @staticmethod
    def _test_and_generate(p:dict[int, int], dataset: Sequence[TimedSequence], ids: Sequence[int], sigma: int, voc:Sequence[int], maxsize:int) -> Sequence[Sequence]:
        """Recursive function to explore the search space of multisets larger than p and extract the frequent ones

        Parameters:
        -----------
        :param p: a multiset pattern (dictionary with items as keys and number of occurrences (>=1) as values)
        :param dataset: dataset
        :param ids: list of identifiers of examples in the dataset (implementation of the dataset projection)
        :param sigma: minimal threshold constraint
        :param voc: list of items that can be used to extend the current multiset
        :param maxsize: maximal size the multiset

        This is a recursive function.
        """
        notin_newids = [ i for i in ids for item,c in p.items() if dataset[i]._data.tolist().count(item)<c ]
        newids = [i for i in ids if i not in notin_newids]
        if len(newids)<sigma:
            #the pattern is not frequent, stop recursion
            return []

        F = [p]
        if len(p)<maxsize:
            for I in voc:
                if max(p)>I:
                    continue
                else:
                    q = p.copy()
                    if max(p)==I:
                        q[I] +=1
                    else:
                        q[I] = 1
                    F = F + ChronicleMiner._test_and_generate(q, dataset, newids, sigma, voc, maxsize)
        return F
    
    @staticmethod
    def MultisetMining(dataset:Sequence[TimedSequence], sigma: int, voc:Sequence, maxsize:int =5) -> Sequence[Sequence]:
        """Function to extract frequent multisets in a database of sequences

        Parameters
        -----------
        :param dataset: list of sets
        :param sigma: minimal frequency threshold

        Depth first search algorithm for mining frequent muultisets. 
        This function call the `test_and_generate` recursive function
        """
        F=[] #frequent patterns
        for q in voc:
            F = F + ChronicleMiner._test_and_generate({q:1}, dataset, [i for i in range(len(dataset))], sigma, voc, maxsize)
        return F


    def __init__(self, minfreq: int, maxlen :int =5, maxgap : Union[float,np.timedelta64] =None):
        """
        Parameters
        -----------
        :param minfreq: minimal frequency threshold (number of sequences supporting a sequence)
        :param maxlen: maximum length of a sequential pattern (number of items)"""
        self.minfreq = minfreq
        self.maxlen = maxlen
        self.maxgap = maxgap
        self.frequentPatterns = []


    def mine(self, db: Sequence[TimedSequence], episodeCounting:bool = False) -> Sequence[Chronicle]:
        """
        Mining function (prefixspan strategy).
        The function can evaluate the support using the number of examples in the database or using episode mining (works with one or more sequences)

        Parameters
        ----------
        :param db: collection of timed sequences
        :param episodeCounting: activate the enumeration of patterns based on its multiple occurrences in a sequence

        Returns
        -------
        A collection of chronicles
        """

        #reinit the patterns
        self.frequentPatterns = []

        #extract vocabulary
        voc=[]
        for seq in db:
            voc += np.unique(seq._data).tolist()
        if not episodeCounting:
            self.vocabulary = [item for item in np.unique(voc) if voc.count(item)>=self.minfreq]
        else:
            for item in voc:
                count=0
                for seq in db:
                    count += seq._data.tolist().count(item)
                if count>=self.minfreq:
                    self.vocabulary.append(item)

        self.db = db

        F=ChronicleMiner.MultisetMining(self.db, self.minfreq, self.vocabulary, self.maxlen)

        #HERE: F is a collection of frequent multisets
        
        return F
"""
        #create the empty pattern
        initPat = SequenceMiner.seqPatInternal()
        initPat.sequence = []
        initPat.idlist = [i for i in range(len(db))]
        initPat.lastPositionPointer = [-1 for i in range(len(db))]
        if episodeCounting: initPat.initPosition = [-1 for i in range(len(db))]

        if len(db)>=self.minfreq:
            self.__expand(initPat, episodeCounting)

        return [ pat.toSequentialPattern() for pat in self.frequentPatterns]"""


if __name__ == "__main__":
    import numpy as np
    seq1 = [
        ("a", 1),
        ("c", 2),
        ("b", 3),
        ("a", 8),
    ]
    seq2 = [
        ("a", 1),
        ("c", 2),
        ("d", 3),
        ("d", 8),
    ]
    seq3 = [
        ("d", 1),
        ("a", 4),
        ("d", 5),
        ("c", 8),
        ("d", 9),
    ]

    db = []
    for seq in [seq1,seq2,seq3]:
        dates = np.array(
            [np.datetime64("1970-01-01") + np.timedelta64(e[1], "D") for e in seq],
            dtype="datetime64",
        )
        data = np.array([e[0] for e in seq])
        ts = TimedSequence(dates, data)
        db.append(ts)

    miner = ChronicleMiner(minfreq=2)

    ret=miner.mine(db)

    for pat in ret:
        print(pat)
"""
    print("with gap constraint")
    miner.maxgap=2
    ret=miner.mine(db)
    for pat in ret:
        print(pat)

    print("episodes")
    miner.maxgap=None
    miner.minfreq=2
    ret=miner.mine(db, episodeCounting=True)

    for pat in ret:
        print(pat)
"""