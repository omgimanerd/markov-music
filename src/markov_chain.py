#!/usr/bin/python
# This class handles the storage and manipulation of a markov chain of notes.

from collections import Counter, defaultdict, namedtuple

import random

Note = namedtuple('Note', ['note', 'duration'])

class MarkovChain:

    def __init__(self):
        self.chain = defaultdict(Counter)
        self.sums = defaultdict(int)

    @staticmethod
    def create_from_dict(dict):
        m = MarkovChain()
        # bugged!
        for from_note, to_notes in dict.items():
            for k, v in to_notes.items():
                m.add(from_note, k, v)
        return m

    def _serialize(self, note, duration):
        return Note(note, duration)

    def __str__(self):
        return str(self.get_chain())

    def add(self, from_note, to_note, duration):
        self.chain[from_note][self._serialize(to_note, duration)] += 1
        self.sums[from_note] += 1

    def get_next(self, seed_note):
        if seed_note is None or seed_note not in self.chain:
            random_chain = self.chain[random.choice(list(self.chain.keys()))]
            return random.choice(list(random_chain.keys()))
        next_note_counter = random.randint(0, self.sums[seed_note])
        for note, frequency in self.chain[seed_note].items():
            next_note_counter -= frequency
            if next_note_counter <= 0:
                return note

    def merge(self, other):
        assert isinstance(other, MarkovChain)
        self.sums = defaultdict(int)
        for from_note, to_notes in other.chain.items():
            self.chain[from_note].update(to_notes)
        for from_note, to_notes in self.chain.items():
            self.sums[from_note] = sum(self.chain[from_note].values())

    def get_chain(self):
        return {k: dict(v) for k, v in self.chain.items()}

    def print_as_matrix(self, limit=10):
        columns = []
        for from_note, to_notes in self.chain.items():
            for note in to_notes:
                if note not in columns:
                    columns.append(note)
        _col = lambda string: '{:<8}'.format(string)
        _note = lambda note: '{}:{}'.format(note.note, note.duration)
        out = _col('')
        out += ''.join([_col(_note(note)) for note in columns[:limit]]) + '\n'
        for from_note, to_notes in self.chain.items():
            out += _col(from_note)
            for note in columns[:limit]:
                out += _col(to_notes[note])
            out += '\n'
        print(out)

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
        m.merge(n)
        print(m)
        m.print_as_matrix()
