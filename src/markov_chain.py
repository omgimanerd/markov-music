#!/usr/bin/python
# This class handles the storage and manipulation of a markov chain.

from collections import defaultdict

import copy

class MarkovChain:

    def __init__(self):
        self.chain = defaultdict(lambda: defaultdict(int))

    @staticmethod
    def create_from_dict(dict):
        m = MarkovChain()
        for from_note, to_notes in dict.items():
            for k, v in to_notes.items():
                m.add(from_note, k, v)
        return m

    def _serialize(self, note, duration):
        return '{}_{}'.format(note, duration)

    def __str__(self):
        return str(self.get_chain())

    def add(self, from_note, to_note, duration):
        self.chain[from_note][self._serialize(to_note, duration)] += 1

    def merge(self, other):
        assert isinstance(other, MarkovChain)
        out = MarkovChain()
        for chain in [self.chain, other.chain]:
            for from_note, to_notes in chain.items():
                for k, v in to_notes.items():
                    out.chain[from_note][k] += v
        return out

    def get_chain(self):
        return {k: dict(v) for k, v in self.chain.items()}

if __name__ == '__main__':
    import sys
    if len(sys.argv) == 2 and sys.argv[1] == 'test':
        m = MarkovChain()
        m.add(12, 14, 200)
        m.add(12, 15, 200)
        m.add(14, 25, 200)
        m.add(12, 14, 200)
        n = MarkovChain()
        n.add(10, 13, 100)
        n.add(12, 14, 200)
        print(m.merge(n))
