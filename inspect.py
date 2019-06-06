#!/usr/bin/python

import mido

def inspect(filename):
    mid = mido.MidiFile(filename)
    for i, track in enumerate(mid.tracks):
        print('Track {}: {}'.format(i, track.name))
        for message in track:
            print(message)

if __name__ == '__main__':
    import sys
    if len(sys.argv) == 2:
        inspect(sys.argv[1])
    else:
        print('Usage: python inspect.py <input.midi>')
