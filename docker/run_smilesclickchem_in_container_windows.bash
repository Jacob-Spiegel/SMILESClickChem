#!/bin/bash
# This script runs SMILESClickChem from within the docker container
# It serves as the ENTRYPOINT of the docker.
/root/miniconda3/bin/python SMILESClickChem/RunSMILESClickChem.py -j /UserFiles/docker_json_vars.json >> /Outputfolder/output.txt 2>> /Outputfolder/error.txt