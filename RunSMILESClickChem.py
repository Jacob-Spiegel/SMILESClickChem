# !/usr/bin/env python

"""This is the executable file for SMILESClickChem. This script should come
first. It should obtain and verify all the parameters work. This than should
pass these parameters variables to the main execution function titled
SMILESClickChemMainExecute.py found in MainFunctions

If you use SMILESClickChem in your research, please cite the following reference:
Spiegel, J.O., Durrant, J.D. AutoGrow4: an open-source genetic algorithm
for de novo drug design and lead optimization. J Cheminform 12, 25 (2020).
[doi: 10.1186/s13321-020-00429-4]
"""

import __future__

import argparse
import copy
import datetime

# Imports of files are burried below to prevent EOF issues in MPI mode

################
# Run SMILESClickChem #
################

PARSER = argparse.ArgumentParser()

# Allows the run commands to be submitted via a .json file.
PARSER.add_argument(
    "--json",
    "-j",
    metavar="param.json",
    help="Name of a json file containing all parameters. \
    Overrides other arguments.",
)

# Allows the run in debug mode. Doesn't delete temp files.
PARSER.add_argument(
    "--debug_mode",
    "-d",
    action="store_true",
    default=False,
    help="Run SMILESClickChem in Debug mode. This keeps all \
    temporary files and adds extra print statements.",
)

# Input/Output directories
PARSER.add_argument(
    "--root_output_folder",
    "-o",
    type=str,
    help="The Path to the folder which all output files will be placed.",
)
PARSER.add_argument(
    "--source_compound_file",
    "-s",
    type=str,
    help="PATH to the file containing the source compounds. It must be \
    tab-delineated .smi file. These ligands will seed the first generation.",
)
PARSER.add_argument(
    "--filter_source_compounds",
    choices=[True, False, "True", "False", "true", "false"],
    default=True,
    help="If True source ligands from source_compound_file will be \
    filter using the user defined filter choices prior to the 1st generation being \
    created. If False, ligands which would fail the ligand filters could seed \
    the 1st generation. Default is True.",
)

# SMILESClickChem Settings
PARSER.add_argument(
    "--max_time_MCS_prescreen",
    type=int,
    default=1,
    help="amount time the pre-screen MCS times out. Time out doesnt prevent \
    mcs matching just takes what it has up to that point",
)
PARSER.add_argument(
    "--max_time_MCS_thorough",
    type=int,
    default=1,
    help="amount time the thorough MCS times out. Time out doesnt prevent \
    mcs matching just takes what it has up to that point",
)
PARSER.add_argument(
    "--min_atom_match_MCS",
    type=int,
    default=4,
    help="Determines the minimum number of atoms in common for a substructurematch. \
    The higher the more restrictive, but the more likely for two ligands not to match",
)
PARSER.add_argument(
    "--protanate_step",
    action="store_true",
    default=False,
    help="Indicates if SMILESClickChem uses protanated mols (if true) or deprot \
    (if False) SMILESClickChem is 10x faster when deprotanated",
)


# Mutation Settings
PARSER.add_argument(
    "--rxn_library",
    choices=["click_chem_rxns", "robust_rxns", "all_rxns", "Custom"],
    default="all_rxns",
    help="This set of reactions to be used in Mutation. \
    If Custom, one must also provide rxn_file Path and function_group_library path",
)
PARSER.add_argument(
    "--rxn_library_file",
    type=str,
    default="",
    help="This PATH to a Custom json file of SMARTS reactions to use for Mutation. \
    Only provide if using the Custom option for rxn_library.",
)
PARSER.add_argument(
    "--function_group_library",
    type=str,
    default="",
    help="This PATH for a dictionary of functional groups to be used for Mutation. \
    Only provide if using the Custom option for rxn_library.",
)
PARSER.add_argument(
    "--complementary_mol_directory",
    type=str,
    default="",
    help="This PATH to the directory containing all the molecules being used \
    to react with. The directory should contain .smi files contain SMILES of \
    molecules containing the functional group represented by that file. Each file \
    should be named with the same title as the functional groups described in \
    rxn_library_file & function_group_library +.smi \
    All Functional groups specified function_group_library must have its \
    own .smi file. We recommend you filter these dictionaries prior to SMILESClickChem \
    for the Drug-likeliness and size filters you will Run SMILESClickChem with.",
)


# processors and multithread mode
PARSER.add_argument(
    "--number_of_processors",
    "-p",
    type=int,
    metavar="N",
    default=1,
    help="Number of processors to use for parallel calculations. Set to -1 for all available CPUs.",
)
PARSER.add_argument(
    "--multithread_mode",
    default="multithreading",
    choices=["mpi", "multithreading", "serial"],
    help="Determine what style \
    multithreading: mpi, multithreading, or serial. serial will override \
    number_of_processors and force it to be on a single processor.",
)

# Populations settings
PARSER.add_argument(
    "--number_of_crossovers",
    type=int,
    default=10,
    help="The number of ligands which will be created via crossover in each \
    generation besides the first",
)
PARSER.add_argument(
    "--number_of_mutants",
    type=int,
    default=10,
    help="The number of ligands which will be created via mutation in each \
    generation besides the first.",
)

####### FILTER VARIABLES
PARSER.add_argument(
    "--LipinskiStrictFilter",
    action="store_true",
    default=False,
    help="Lipinski filters for orally available drugs following Lipinski rule of fives. \
    Filters by molecular weight, logP and number of hydrogen bond donors and acceptors. \
    Strict implementation means a ligand must pass all requirements.",
)
PARSER.add_argument(
    "--LipinskiLenientFilter",
    action="store_true",
    default=False,
    help="Lipinski filters for orally available drugs following Lipinski rule of fives. \
    Filters by molecular weight, logP and number of hydrogen bond donors and acceptors. \
    Lenient implementation means a ligand may fail all but one requirement and still passes.",
)
PARSER.add_argument(
    "--GhoseFilter",
    action="store_true",
    default=False,
    help="Ghose filters for drug-likeliness; filters by molecular weight,\
    logP and number of atoms.",
)
PARSER.add_argument(
    "--GhoseModifiedFilter",
    action="store_true",
    default=False,
    help="Ghose filters for drug-likeliness; filters by molecular weight,\
    logP and number of atoms. This is the same as the GhoseFilter, but \
    the upper-bound of the molecular weight restrict is loosened from \
    480Da to 500Da. This is intended to be run with Lipinski Filter and \
    to match AutoGrow 3's Ghose Filter.",
)
PARSER.add_argument(
    "--MozziconacciFilter",
    action="store_true",
    default=False,
    help="Mozziconacci filters for drug-likeliness; filters by the number of \
    rotatable bonds, rings, oxygens, and halogens.",
)
PARSER.add_argument(
    "--VandeWaterbeemdFilter",
    action="store_true",
    default=False,
    help="VandeWaterbeemd filters for drug likely to be blood brain barrier permeable. \
    Filters by the number of molecular weight and Polar Sureface Area (PSA).",
)
PARSER.add_argument(
    "--PAINSFilter",
    action="store_true",
    default=False,
    help="PAINS filters against Pan Assay Interference Compounds using \
    substructure a search.",
)
PARSER.add_argument(
    "--NIHFilter",
    action="store_true",
    default=False,
    help="NIH filters against molecules with undersirable functional groups \
    using substructure a search.",
)
PARSER.add_argument(
    "--BRENKFilter",
    action="store_true",
    default=False,
    help="BRENK filter for lead-likeliness, by matching common false positive \
    molecules to the current mol.",
)
PARSER.add_argument(
    "--No_Filters",
    action="store_true",
    default=False,
    help="No filters will be applied to compounds.",
)
PARSER.add_argument(
    "--alternative_filter",
    action="append",
    help="If you want to add Custom filters to the filter child classes \
    Must be a list of lists \
    [[name_filter1, Path/to/name_filter1.py],[name_filter2, Path/to/name_filter2.py]]",
)

# gypsum # max variance is the number of conformers made per ligand
PARSER.add_argument(
    "--convert_to_3D",
    action="store_true",
    default=False,
    help="Whether we will convert SMILES to 3D SDFs and PDB using Gypsum-DL \
    default is True; PDBs are stored at PATH\Run_0\PDBs\; \
    3D SDF files are stored at PATH\Run_0\3D_SDFs\ \
    If False newly created compounds will only be \
    output as SMILES in NEW_SMILES.smi",
)
PARSER.add_argument(
    "--max_variants_per_compound",
    type=int,
    default=3,
    help="number of conformers made per ligand. \
    See Gypsum-DL publication for details",
)
PARSER.add_argument(
    "--gypsum_thoroughness",
    "-t",
    type=str,
    help="How widely Gypsum-DL will search for \
    low-energy conformers. Larger values increase \
    run times but can produce better results. \
    See Gypsum-DL publication for details",
)
PARSER.add_argument(
    "--min_ph",
    metavar="MIN",
    type=float,
    default=6.4,
    help="Minimum pH to consider.See Gypsum-DL \
    and Dimorphite-D publication for details.",
)
PARSER.add_argument(
    "--max_ph",
    metavar="MAX",
    type=float,
    default=8.4,
    help="Maximum pH to consider.See Gypsum-DL \
    and Dimorphite-D publication for details.",
)
PARSER.add_argument(
    "--pka_precision",
    metavar="D",
    type=float,
    default=1.0,
    help="Size of pH substructure ranges. See Dimorphite-DL \
    publication for details.",
)
PARSER.add_argument(
    "--gypsum_timeout_limit",
    type=float,
    default=15,
    help="Maximum time gypsum is allowed to run for a given ligand in seconds. \
    On average Gypsum-DL takes on several seconds to run for a given ligand, but \
    factors such as mol size, rotatable bonds, processor speed, and gypsum \
    settings (ie gypsum_thoroughness or max_variants_per_compound) will change \
    how long it takes to run. If increasing gypsum settings it is best to increase \
    the gypsum_timeout_limit. Default gypsum_timeout_limit is 15 seconds",
)

# Reduce files down. This compiles and compresses the files in the PDBs folder
# makes data transfer quicker, but requires running the
# file_concatenation_and_compression.py in the Utility script folder to
# separate these files out for readability.
PARSER.add_argument(
    "--reduce_files_sizes",
    choices=[True, False, "True", "False", "true", "false"],
    default=True,
    help="Run this combines all files in the PDBs folder into a \
    single text file. Useful when data needs to be transferred.",
)

# mpi mode pre-Run so there are python cache files without EOF Errors
PARSER.add_argument(
    "--cache_prerun",
    "-c",
    action="store_true",
    help="Run this before running gypsum in mpi-mode.",
)

args_dict = vars(PARSER.parse_args())

# copying args_dict so we can delete out of while iterating through the
# original args_dict
INPUTS = copy.deepcopy(args_dict)

for k, v in args_dict.items():
    if v is None:
        del INPUTS[k]

if args_dict["cache_prerun"] is False:

    start_time = str(datetime.datetime.now())
    # load the commandline parameters
    from SMILESClickChem.user_vars import load_in_commandline_parameters

    vars, printout = load_in_commandline_parameters(INPUTS)

    # print out the UserVars for the record
    print("\n=====================================================")
    print("==============   Parameters as list:  ===============")
    for key in list(vars.keys()):
        print(key, vars[key])
    print("\n=====================================================")
    print("===========   Parameters as dictionary:  ============")
    print(vars)
    print("=====================================================")
    print("=====================================================\n\n")

    # Run SMILESClickChem. Import move here to prevent EOF in MPI mode. importing
    # files before the Parallelizer class is established in MPI mode can have
    # errors
    import SMILESClickChem.SMILESClickChem_main_execute as SMILESClickChemMainExecute

    SMILESClickChemMainExecute.main_execute(vars)

    # Print completion message

    printout = "\nSMILESClickChem run started at:   {}\nSMILESClickChem ".format(start_time)
    printout = printout + "run completed at: {}\n".format(str(datetime.datetime.now()))
    print(printout)

    print("SMILESClickChem FINISHED")

    # # kill mpi workers
    vars["parallelizer"].end(vars["multithread_mode"])


else:  # cache prerun. This is necessary to prevent race conditions in mpi mode.
    import SMILESClickChem.user_vars
    import SMILESClickChem.SMILESClickChem_main_execute as SMILESClickChemMainExecute
    import SMILESClickChem.operators.convert_files.gypsum_dl.gypsum_dl.Parallelizer