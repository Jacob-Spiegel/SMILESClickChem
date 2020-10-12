# Docker Instructions

This directory contains the scripts to run SMILESClickChem within a docker
container. This is useful when using an operating system that is not
compatible with the SMILESClickChem dependencies or that is not supported by our
current multithreading approach, such as Windows.

Before running these scripts, beb sure to install [docker
software](https://www.docker.com/products/docker-desktop). Please also always
run these scripts with ***sudo*** (Linux/macOS) or ***administrative
privileges*** (Windows).

It takes a few minutes longer to run SMILESClickChem with docker the first time. The
same is true if docker images have been recently purged. The script must
install the dependencies within the docker environment.

Depending on the SMILESClickChem settings, processor speed/count, etc., SMILESClickChem
may complete within minutes or may take as long as multiple days. Please run
the container using the appropriate settings so that it can complete without
being disrupted or disruptive. Using `nohup` may be useful when executing
longer runs or when running jobs remotely (i.e., over `ssh`).

## Run instructions

To run SMILESClickChem in a docker, please use the `smilesclickchem_in_docker.py` script:

1. Example on Linux/MacOS:
   1. Change into the `docker` directory in a bash terminal `cd
      SMILESClickChem/docker/`
   2. Run `smilesclickchem_in_docker.py` with ***sudo*** and supply a json file using
      the normal pathing of your system, i.e., `sudo python
      smilesclickchem_in_docker.py -j ./examples/sample_smilesclickchem_docker_json.json`
      - Results will be output to the directory specified by the
        `root_output_folder` variable.

2. Example on Windows OS:
   1. Open a docker-enabled and bash-enabled terminal with ***administrative
      privileges***.
   2. Change into the `docker` directory in a bash terminal `cd
      SMILESClickChem/docker/`
   3. Run `smilesclickchem_in_docker.py` using the normal pathing of your system,
      i.e., `python smilesclickchem_in_docker.py -j
      ./examples/sample_smilesclickchem_docker_json.json`
      - Results will be output to the directory specified by the
        `root_output_folder` variable.

## Files

### For Use in the Host System

- `smilesclickchem_in_docker.py`: Runs SMILESClickChem from within docker. Launches a docker
  image. Accepts the exact same parameters as SMILESClickChem, with the following
  exceptions:
  - User variables must be supplied in JSON format.
    - Please see documentation within the tutorial manual, where an example
      can be found: `./examples/sample_smilesclickchem_docker_json.json`
  - Required variables within the JSON file:
    - `-root_output_folder`: folder path on host system that results will be
      copied to.
    - `-source_compound_file`: Path on host system to the tab-delineated .smi
      file that will seed generation 1.
- `examples/example.bash`: An example of how to run `smilesclickchem_in_docker.py`.
- `examples/sample_smilesclickchem_docker_json.json`: A sample JSON file to supply to
  `smilesclickchem_in_docker.py`.

### For Use in Docker

- `run_smilesclickchem_in_container.bash`: The docker image's ENTRYPOINT runs this
  script.
- `run_smilesclickchem_in_container_windows.bash`: The windows version of docker
  image's ENTRYPOINT runs this script. It is automatically switched by
  `smilesclickchem_in_docker.py`
- `Dockerfile`: Docker instructions re. how to build the image.


### Developer Notes

- SMILESClickChem's Docker has been tested and fixed to install the following dependencies:
  ```python
  >>> rdkit.__version__
  '2020.03.1'
  >>> numpy.__version__
  '1.18.1'
  >>> scipy.__version__
  '1.4.1'
  >>> func_timeout.__version__
  '4.3.5'
  ```

- Please test and update `$PATH/docker/Dockerfile` these as new versions of SMILESClickChem and
  these dependencies are released.