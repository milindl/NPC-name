## NPC-name

### Motivation
* Daniel -> Daneel in an Isaac Asimov book.
* Alignment of protien sequences

### Running
This kind of a small modification in the name leads to many possibilities for making NPC names from a "seed" name.
A complete writeup is in the works, here's how to use it:

1. Change a few parameters in the method fn(). The first array in the argument to n_m.match is the "seed". It needs to be specified in the IPA, which one can look up at [http://www.antimoon.com/resources/phonchart2008.pdf](http://www.antimoon.com/resources/phonchart2008.pdf)

2. The 3rd parameter to GeneticAlgorithm needs to be [x-1, x, x+1] where x is the length of your "seed". You can change it later when I document completely and/or you read it.

3. Run
```python name_gen```

### TODO:
* Improve useability
* Documentation and writeup