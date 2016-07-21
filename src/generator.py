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
            random_note = random.choice(random_chain.keys())
            while random_note == "sum":
                random_note = random.choice(random_chain.keys())
            return random_note
        next_note_counter = random.randint(
            0, self.markov_chain[current_note]["sum"])
        for note, frequency in self.markov_chain[
                current_note].iteritems():
            if note != "sum":
                next_note_counter -= frequency
                if next_note_counter <= 0:
                    return note

    def _note_to_message(self, serialized_note):
        parts = serialized_note.split("_")
        return mido.Message('note_on', note=int(parts[0]), velocity=127,
                            time=int(parts[1]))

    def generate(self, filename):
        with mido.midifiles.MidiFile() as midi:
            track = mido.MidiTrack()
            last_note = None
            for i in range(100):
                new_serialized_note = self._get_next_note(last_note)
                last_note = int(new_serialized_note.split("_")[0])
                track.append(self._note_to_message(new_serialized_note))
            midi.tracks.append(track)
            midi.save(filename)

if __name__ == "__main__":
    from serializer import Serializer
    chain = Serializer("midi/river_flows.mid").get_markov_chain()
    print "Generated markov chain"
    print chain
    Generator(chain).generate("out.mid")
