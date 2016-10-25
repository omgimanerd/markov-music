# markov-music

This repository contains code that analyzes MIDI tracks and generates a markov
chain based on the note sequences in the MIDI.

## Setup
```
pip install -r requirements.txt
```

## Methodology
For reference on the structure of the bits in a MIDI, see this
[link](http://www.music-software-development.com/midi-tutorial.html)

After separating the tracks in the MIDI, we iterate through to group notes
into what we will call "chunks". We generate the markov chain using this
progression of chunks by permuting all the notes in one chunk to the next and
using each permutation as a link in the markov chain.
We serialize each note and its duration into a string of the form
"*note*_*duration-in-ms*". Eg: "60_500"
The notes are numbers from 0-127 where 60 is middle C (MIDI standard).

## Contributing
Fork this repository and clone it to your own computer. Send me a pull request
with interesting thoughts, ideas, or suggestions.
Please follow the [PEP8](http://pep8.org) standard if you are contributing
to the codebase. Avoid pushing large midi files if possible.

## Contributors
Alvin Lin (omgimanerd)
