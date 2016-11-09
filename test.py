#!/usr/bin/python

import mido

mid = mido.MidiFile("midi/river_flows.mid")

print mid

track1 = None
track2 = None

for i, track in enumerate(mid.tracks):
    print('Track {}: {}'.format(i, track.name))
    for message in track[:75]:
        print(message)


with mido.midifiles.MidiFile() as midi:
    track = mido.MidiTrack()

    def add(note, velocity, time):
        track.append(mido.Message('note_on', note=note,
                                  velocity=velocity,
                                  time=time))

    add(72, 100, 0)
    add(64, 100, 0)
    add(62, 100, 500)
    add(62, 0, 2000)
    add(60, 100, 1000)
    add(62, 100, 1000)
    add(64, 100, 1000)
    add(64, 100, 1000)
    add(64, 100, 1000)
    add(64, 0, 1000)
    # add(81, 71, 0)
    # add(54, 72, 1000)
    # add(81, 0, 1000)
    # add(54, 0, 0)

    midi.tracks.append(track)
    midi.save('new_song.mid')
