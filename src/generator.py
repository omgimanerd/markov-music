#!/usr/bin/python
# This class handles the generation of a new song given a markov chain
# containing the note transitions and their frequencies.

import random
import mido

class Generator:

    def __init__(self, markov_chain, sums):
        self.markov_chain = markov_chain
        self.sums = {}

    @staticmethod
    def load(markov_chain):
        sums = { k: sum(v.values()) for k, v in markov_chain.items() }
        return Generator(markov_chain, sums)

    def _get_next_note(self, current_note=None):
        if current_note is None or current_note not in self.markov_chain:
            random_chain = self.markov_chain[
                random.choice(list(self.markov_chain.keys()))]
            random_note = random.choice(list(random_chain.keys()))
            parts = random_note.split('_')
            return {
                'note': int(parts[0]),
                'duration': int(parts[1])
            }
        # This counter is a random number from which we subtract note
        # frequencies in order to generate the next note in our chain.
        next_note_counter = random.randint(
            0, self.sums[current_note])
        for note, frequency in self.markov_chain[current_note].items():
            next_note_counter -= frequency
            if next_note_counter <= 0:
                return note

    def _note_to_message(self, note):
        return mido.Message('note_on',
                            note=note['note'],
                            velocity=127,
                            time=note['duration'])

    def generate(self, filename):
        with mido.midifiles.MidiFile() as midi:
            track = mido.MidiTrack()
            last_note = None
            for i in range(100):
                new_note = self._get_next_note(last_note)
                track.append(self._note_to_message(new_note))
            midi.tracks.append(track)
            midi.save(filename)

if __name__ == "__main__":
    import sys
    if len(sys.argv) == 3:
        from parser import Parser
        chain = Parser(sys.argv[1]).get_chain()
        print("Generated markov chain")
        Generator.load(chain).generate(sys.argv[2])
