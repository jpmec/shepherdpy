shepherdpy
==========

A companion library for mincemeatpy that will manage MapReduce clients.

You can get mincemeatpy here:

https://github.com/michaelfairley/mincemeatpy

Why?
----

mincemeatpy is a small, lightweight MapReduce library for Python.
It doesn't provide functionality for managing processes.

shepherdpy makes it easy to manage mincemeatpy clients.


First Example
-------------

This is the simplest example. It will use the identical dataset from [the mincemeat.py example](https://github.com/michaelfairley/mincemeatpy).


First, start the server:

```bash
python example.py
```

Second, start the client:

```bash
python shepherd.py
```

And the server will print out:

```python
{'a': 2, 'on': 1, 'great': 1, 'Humpty': 3, 'again': 1, 'wall': 1, 'Dumpty': 2, 'men': 1, 'had': 1, 'all': 1, 'together': 1, "King's": 2, 'horses': 1, 'All': 1, "Couldn't": 1, 'fall': 1, 'and': 1, 'the': 2, 'put': 1, 'sat': 1}
```


Notice that shepherd.py supplies reasonable default values to mincemeat,
so it is easier to start the mincemeat clients.


Notes
-----

mincemeat.py 0.1.3 is included in this repo.  It is for testing and demo
purposes only.  It is recommended you use the official mincemeat.py version
from the [repo](https://github.com/michaelfairley/mincemeatpy).
