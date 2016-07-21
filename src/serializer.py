#!/usr/bin/python
# This class handles the serialization of a midi and generates a
# dictionary holding a markov chain of the notes in the midi.

import hashlib
import mido

class Serializer:

    def __init__(self, filename):
        """
        This is the constructor for a Serializer, which will serialize
        a midi given the filename and generate a markov chain of the
        notes in the midi.
        """
        self.filename = filename
        # The tempo is number representing the number of microseconds
        # per beat.
        self.tempo = None
        # The delta time between each midi message is a number that
        # is a number of ticks, which we can convert to beats using
        # ticks_per_beat.
        self.ticks_per_beat = None
        self.markov_chain = {}
        self.counter = 0
        self._serialize()

    def _serialize(self):
        """
        This function handles the reading of the midi and chunks the
        notes into sequenced "chords", which are inserted into the
        markov chain.
        """
        midi = mido.MidiFile(self.filename)
        self.ticks_per_beat = midi.ticks_per_beat
        previous_chunk = []
        current_chunk = []
        for i, track in enumerate(midi.tracks):
            for message in track:
                if message.type == "set_tempo":
                    self.tempo = message.tempo
                elif message.type == "note_on":
                    if message.time == 0 and message.velocity != 0:
                        current_chunk.append(message.note)
                    else:
                        if len(previous_chunk) == 0:
                            previous_chunk = current_chunk
                            current_chunk == 0
                        else:
                            self._sequence(previous_chunk,
                                           current_chunk,
                                           message.time)

    def _sequence(self, previous_chunk, current_chunk, duration):
        """
        Given the previous chunk and the current chunk of notes as well
        as an averaged duration of the current notes, this function
        permutes every combination of the previous notes to the current
        notes and sticks them into the markov chain.
        """
        for n1 in previous_chunk:
            if n1 not in self.markov_chain:
                self.markov_chain[n1] = {}
            for n2 in current_chunk:
                note = "%s_%s" % (n2, self._bucket_duration(duration))
                self.markov_chain[n1][note] = self.markov_chain[n1].get(
                    note, 0) + 1
                self.markov_chain[n1]['sum'] = self.markov_chain[n1].get(
                    'sum', 0) + 1

    def _bucket_duration(self, ticks):
        """
        This method takes a tick count and converts it to a time in
        milliseconds, bucketing it to the nearest 250 milliseconds.
        """
        try:
            ms = ((ticks / self.ticks_per_beat) * self.tempo) / 1000
            return ms - (ms % 250) + 250
        except TypeError:
            raise TypeError(
                "Could not read a tempo and ticks_per_beat from midi")

    def get_markov_chain(self):
        return self.markov_chain


if __name__ == "__main__":
    print Serializer("midi/river_flows.mid").get_markov_chain()
