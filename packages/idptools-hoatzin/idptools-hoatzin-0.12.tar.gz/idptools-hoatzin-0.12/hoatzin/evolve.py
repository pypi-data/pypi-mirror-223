# user facing functionality

# add functions here
__all__ = ['sequence']

from hoatzin.hoatzin_exceptions import HoatzinException
from hoatzin.backend.evolution_tools import evolve_sequence as _evolve_sequence


# ..........................................................................................
#
def sequence(seq, number_generations, mutations_per_generation=1, mutation_probs=None,
    sequence_type='protein_sequence', codon_probs=None, return_all_seqs=False):
    '''
    Function that takes in a sequence and returns a mutated sequence
    based on the mutation probabilities passed in. If no mutation_probs
    input, will default to the COSMIC 2023 values. 

    Parameters
    ----------------
    seq : str
        Valid protien or nucleic acid sequence

    number_generations : int
        number of genreations to mutate the sequence. Assumes 1 mutation per generation.

    mutations_per_generation : int
        number of mutations in each generation

    mutation_probs : dict
        Probabilities for each mutation. Look at 
        hoatzin_parameters.NUCLEOTIDE_MUTATION_PROBS for an example
        Defautls to human. 

    sequence_type : str
        Either 'protein_sequence' or 'nucleotide_sequence'
        Determines if is nucleotides or protein
        Defaults to protien.  

    codon_probs : dict
        Probabilities for each codon for each amino acid if a protein seq is input. Look at
        hoatzin_parameters.CODON_PROBABILITIES['human'] for an example.
        Defaults to human. 

    return_all_seqs : bool
        If true, returns a list of all sequences. If false, returns only the final sequence. 

    Returns
    -------------
    str or dict
        Returns a mutated sequence or dict of mutated seqs if
        return_all_seqs is set to True
    '''
    
    return _evolve_sequence(seq=seq, number_generations=number_generations, 
        mutations_per_generation=mutations_per_generation, mutation_probs=mutation_probs,
        sequence_type=sequence_type, codon_probs=codon_probs, return_all_seqs=return_all_seqs)




