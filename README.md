qcd
===

This simple little script can be used to quickly move between locations saved in a database.


Installation
------------

  1. Move the python scripts into a comfortable place
  2. Set the path in `sh_hook` to point to said place
  3. Source `sh_hook` into your shell or add it into your starup script for automatic sourcing

Usage
-----

First save a location you visit frequently

```
qcd -a /etc/init.d
```
This will save it into the database at an automatically generated key, which is incrementing integers, so we will save this to 1 in this case.

Or we could have given it a name of our own:
```
qcd -a i /etc/init.d
```

Then whenever we want to go there we can simply write:
```
qcd i
```

To list our saved locations, simply issue:
```
qcd -l
```
and for more operations you might find
```
qcd -h
```
helpful, our you can fork it and write any functionality that is missing! :)

