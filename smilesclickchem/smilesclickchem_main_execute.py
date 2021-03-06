"""
Top level for running SMILESClickChem.
Runs all population generation (operations).
Runs plotting at end.
"""
import __future__

import sys

import smilesclickchem.operators.operations as operations

def main_execute(vars):
    """
    This function takes the user variables and runs SMILESClickChem

    Inputs:
    :param dict vars: dict of user variables which will govern how the
        programs runs
    """

    # Unpack necessary variables
    # output_directory is the root output folder for the run
    output_directory = vars["output_directory"]

    # This will run operations which will:
    # 1)  generate new ligands
    # 2) optionally filter ligands
    # 3) optionally convert from 1D smiles to 3D (mol2/PDB)

    sys.stdout.flush()


    smile_file_new_gen, new_gen_ligands_list = operations.populate_generation(vars)
    sys.stdout.flush()

    if new_gen_ligands_list is None:
        raise ValueError("Population failed to make enough mutants... \
                            Errors could include not enough diversity, too few seeds to the generation, \
                            number_of_mutants is too high, \
                            or all of the seed lack functional groups for performing reactions.")

    sys.stdout.flush()
#
