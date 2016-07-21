#!/usr/bin/python
# This class handles the storage of the generated markov chains as JSON files.

import json

class JSONHandler:

    @staticmethod
    def markov_to_json(markov_chain):
        return json.dumps({
            "version": 1,
            "type": "markov_chain",
            "data": markov_chain
        }, sort_keys=True, indent=4)

    @staticmethod
    def merge_markov_chains(chain1, chain2):
        for key, value in chain2.iteritems():
            if key in chain1:
                chain1[key] = value
            else:
                chain1[key].update(value)
        return chain1

if __name__ == "__main__":
    from serializer import Serializer
    print Serializer("river_flows.mid").get_markov_chain()
