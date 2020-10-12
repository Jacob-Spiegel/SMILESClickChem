#!/bin/bash

# This script runs SMILESClickChem from within the docker container
# It serves as the ENTRYPOINT of the docker.

if echo $* | grep -q "test"; then
  exit;
fi

if echo $* | grep -q "Run"; then
    function my_date {
    date "+%m_%d_%y"
    }

    # chmod -R a+rwx Outputfolder/
    echo "Running SMILESClickChem"

    date_time=$(my_date)

    run_num="${3//"--"/}__"

    error=__error.txt
    output=__output.txt
    Outputfolder=/Outputfolder/$run_num

    output_file=$Outputfolder$date_time$output
    error_file=$Outputfolder$date_time$error

    # Add spacer on log files
    if test -f "$output_file"; then
        echo "" >> $output_file
        echo "" >> $output_file
        echo "" >> $output_file
        echo "###################################\n" >> $output_file
        echo "CONTINUE PREVIOUS SMILESClickChem RUN AT: " >> $output_file
        date >> $output_file
        echo "###################################\n" >> $output_file
        echo "" >> $output_file
        echo "" >> $output_file
        echo "" >> $output_file
    fi
    if test -f "$error_file"; then
        echo "" >> $error_file
        echo "" >> $error_file
        echo "" >> $error_file
        echo "###################################\n" >> $error_file
        echo "CONTINUE PREVIOUS SMILESClickChem RUN AT: " >> $error_file
        date >> $error_file
        echo "###################################\n" >> $error_file
        echo "" >> $error_file
        echo "" >> $error_file
        echo "" >> $error_file
    fi

    echo "/root/miniconda3/bin/python SMILESClickChem/RunSMILESClickChem.py -j /UserFiles/docker_json_vars.json >> $output_file 2> $error_file"
    # Run SMILESClickChem
    /root/miniconda3/bin/python SMILESClickChem/RunSMILESClickChem.py \
        -j /UserFiles/docker_json_vars.json >> $output_file 2>> $error_file

    echo "Completed SMILESClickChem Run"
    # chmod -R a+rwx Outputfolder/
fi
exit
# For interactive/debug add bottom line
# bash

