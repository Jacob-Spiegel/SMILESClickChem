# SMILESClickChem

SMILESClickChem is a cheminformatic, Python program for that reacts one parent ligand (SMILES string) following predefined reactions to create a child compound. SMILESClickChem uses the mutation algorithm from the program AutoGrow4.

SMILESClickChem accepts a list of SMILES (in .smi format) and will attempt to produce a user defined number of unique children SMILES. SMILESClickChem also allows users to apply chemical property filters. Additionally, SMILESClickChem options the automated conversion of the children from 1/2D SMILES to 3D representations (PDB and 3D-SDF) using Gypsum-DL.

# Acknowledgment and Citing

Much of this code is take directly and/or adapted from AutoGrow4. This program also relies on Gypsum-DL and Dimorphite-DL for ligand handling and multiprocessing. Please remember to cite the following papers:

## SMILESClickChem Citation:
    
- Citation Pending

## AutoGrow4 Citation:

- Spiegel, J.O., Durrant, J.D. AutoGrow4: an open-source genetic algorithm for de novo drug design and lead optimization. J Cheminform 12, 25 (2020). [doi: 10.1186/s13321-020-00429-4]

## Gypsum-DL Citation:

- Ropp, P.J., Spiegel, J.O., Walker, J.L. et al. Gypsum-DL: an open-source program for preparing small-molecule libraries for structure-based virtual screening. J Cheminform 11, 34 (2019). https://doi.org/10.1186/s13321-019-0358-3

## AutoGrow4 Dimorphite-DL:

- Ropp, P.J., Kaminsky, J.C., Yablonski, S. et al. Dimorphite-DL: an open-source program for enumerating the ionization states of drug-like small molecules. J Cheminform 11, 14 (2019). https://doi.org/10.1186/s13321-019-0336-9
