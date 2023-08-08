hoatzin
==============================

A Python package for DNA-based evolution of protien sequences. Holistic apprOach for SequAnces To underZtand evolutIoN.

### Last updated August 2023

## Current version: v0.12

## Installation

The current stable version of **hoatzin** is available through GitHub or the Python Package Index (PyPI). 

To install from PyPI, run:

    pip install idptools-hoatzin


You can also install the current development version from

    pip install git+https://git@github.com/idptools/hoatzin

To clone the GitHub repository and gain the ability to modify a local copy of the code, run

    git clone https://github.com/idptools/hoatzin.git
    cd hoatzin
    pip install -e .


## Usage

First import hoatzin

    from hoatzin import evolve

### Evolving Sequences

The ``evolve.sequence()`` function lets you evolve protein or DNA sequences. If you input a protein sequence, it will be turned into a DNA sequence using the codon usage frequencies from humans. The probabilities for each mutation then use nucleotide mutation probabilities that are from COSMIC 2023, which examined the frequencies of non-synonymous mutations in the human genome. The ``evolve.sequence()`` function requires that you input a sequence as the first argument and then the number of generations as the second argument. 1 DNA mutation per generation is assumed.


    sequence='QQQGSRGSGSGRRRGSGSGQGS'
    evolved_sequence = evolve.sequence(sequence, number_generations=10)
    print(evolved_sequence)


Which would return something like:

    QQQGPSGSRNGRRRGFSGGLDS

**Optional Arguments**:

Using the ``evolve.sequence()`` function, you can specify additional parameters.
*mutations_per_generation* - the number of DNA mutations in each 'mutation' generation.
*mutation_probs* - The probabilities of each mutation. You can specify your own dictionary of mutations. See NUCLEOTIDE_MUTATION_PROBS in hoatzin_parameters to specify this. 
*sequence_type* - Lets you specify if you want to mutate a DNA sequence or a protein sequence. You must specify as 'nucleotide_sequence' if you are inputting a nucleotide sequence. 
*codon_probs* - Lets you specify the probabilities of each codon when going from a protein sequence to a DNA sequence. 
*return_all_seqs* - Lets you specify whether to return all sequences generated (one sequence per generation) or just get back a single final sequence. 

**Example**


    sequence='QQQGSRGSGSGRRRGSGSGQGS'
    evolved_sequence = evolve.sequence(sequence, number_generations=10, return_all_seqs=True)
    print(evolved_sequence)

Would return something like...

    {'original': 'QQQGSRGSGSGRRRGSGSGQGS', 1: 'QQQGSRGSGSGHRRGSGSGQGS', 2: 'QQQGSRGSGSGHRRGSGSGQGS', 3: 'QQQGSRGSGSGHKRGSGSGQGS', 4: 'QQQGSRGSGSGDKRGSGSGQGS', 5: 'QRQGSRGSGSGDKRGSGSGQGS', 6: 'QRQGSRGSGSGDKRGSGSGQGL', 7: 'QRQGSRGFGSGDKRGSGSGQGL', 8: 'QRQGSRGFRSGDKRGSGSGQGL', 9: 'QREGSRGFRSGDKRGSGSGQGL', 10: 'QREG*RGFRSGDKRGSGSGQGL'}

### Copyright

Copyright (c) 2023, Ryan Emenecker - Holehouse Lab


#### Acknowledgements
 
Project based on the 
[Computational Molecular Science Python Cookiecutter](https://github.com/molssi/cookiecutter-cms) version 1.1.
