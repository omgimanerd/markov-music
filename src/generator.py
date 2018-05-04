#!/usr/bin/python
# This class handles the generation of a new song given a markov chain
# containing the note transitions and their frequencies.

from markov_chain import MarkovChain

import random
import mido

class Generator:

    def __init__(self, markov_chain):
        self.markov_chain = markov_chain

    @staticmethod
    def load(markov_chain):
        assert isinstance(markov_chain, MarkovChain)
        return Generator(markov_chain)

    def _note_to_messages(self, note):
        return [
            mido.Message('note_on', note=note.note, velocity=127,
                         time=0),
            mido.Message('note_off', note=note.note, velocity=0,
                         time=note.duration)
        ]

    def generate(self, filename):
        with mido.midifiles.MidiFile() as midi:
            track = mido.MidiTrack()
            last_note = None
            for i in range(100):
                new_note = self.markov_chain.get_next(last_note)
                track.extend(self._note_to_messages(new_note))
            midi.tracks.append(track)
            midi.save(filename)

if __name__ == "__main__":
    import sys
    if len(sys.argv) == 3:
        # python generator.py in.mid out.mid
        from parser import Parser
        chain = Parser(sys.argv[1]).get_chain()
        Generator.load(chain).generate(sys.argv[2])
        print("Generated markov chain")
