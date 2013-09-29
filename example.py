#!/usr/bin/env python
import shepherd

data = ["Humpty Dumpty sat on a wall",
        "Humpty Dumpty had a great fall",
        "All the King's horses and all the King's men",
        "Couldn't put Humpty together again",
        ]

datasource = dict(enumerate(data))

def mapfn(k, v):
    for w in v.split():
        yield w, 1

def reducefn(k, vs):
    result = sum(vs)
    return result


if __name__ == '__main__':

    options = {
        'datasource': datasource,
        'mapfn': mapfn,
        'reducefn': reducefn
    }

    results = shepherd.run_server(options)
    print results
