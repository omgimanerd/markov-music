#!/usr/bin/python

import hashlib
import mido

class Serializer:

    def __init__(self, filename):
        self.filename = filename
        # The tempo is number representing the number of microseconds
        # per beat.
        self.tempo = None
        # The delta time between each midi message is a number that
        # is a number of ticks, which we can convert to beats using
        # ticks_per_beat.
        self.ticks_per_beat = None
        self.sequence = {}
        self.counter = 0
        self._serialize()

    def _serialize(self):
        midi = mido.MidiFile(self.filename)
        self.ticks_per_beat = midi.ticks_per_beat
        previous_chunk = []
        current_chunk = []
        for i, track in enumerate(midi.tracks):
            for message in track[:15]:
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
        for n1 in previous_chunk:
            if n1 not in self.sequence:
                self.sequence[n1] = {}
            for n2 in current_chunk:
                note = "%s_%s" % (n2, self._bucket_duration(duration))
                print self.sequence
                self.sequence[n1][note] = self.sequence[n1].get(
                    note, 0) + 1

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

    def __iter__(self):
        return self

    def next():
        if self.counter >= len(self.sequence):
            raise StopIteration()
        self.counter += 1
        return self.sequence[self.counter]


if __name__ == "__main__":
    print Serializer("midi/river_flows.mid").sequence
