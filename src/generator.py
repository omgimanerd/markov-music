#!/usr/bin/python
# This class handles the generation of a new song given a markov chain
# containing the note transitions and their frequencies.

import random
import mido

class Generator:

    def __init__(self, markov_chain):
        self.markov_chain = markov_chain

    def _get_next_note(self, current_note=None):
        if not current_note or current_note not in self.markov_chain:
            random_chain = random.choice(self.markov_chain.values())
            return random.choice(random_chain.keys())
        next_note_counter = random.randint(
            0, self.markov_chain[current_note]["sum"])
        for note, frequency in self.markov_chain[
                current_note].iteritems():
            if note != "sum":
                next_note_counter -= frequency
                if next_note_counter <= 0:
                    return note

    def _parse_note(self, serialized_note):
        print serialized_note
        parts = serialized_note.split("_")
        return mido.Message('note_on', note=int(parts[0]), velocity=127,
                            time=int(parts[1]))

    def generate(self, filename):
        with mido.midifiles.MidiFile() as midi:
            track = mido.MidiTrack()
            for i in range(100):
                print self._get_next_note()
                track.append(self._parse_note(self._get_next_note()))
            midi.tracks.append(track)
            midi.save(filename)

if __name__ == "__main__":
    from serializer import Serializer
    chain = Serializer("midi/river_flows.mid").get_markov_chain()

    Generator(chain).generate("out.mid")
