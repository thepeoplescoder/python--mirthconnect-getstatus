#!/usr/bin/python
#
# This script is used to get the status of each installed
# instance of Mirth Connect on my machine.
#
# 12/7/2015 by Austin Cathey

# Imports
import os
import sys
import subprocess

# Get the directory in which this script resides.
# The requirement is that this script must exist in
# the same directory as all of the instances of Mirth
# Connect that you wish to run.
SCRIPT_DIR = os.path.dirname(os.path.realpath(__file__))

# Here we're going to populate the statuses variable.
#
# We need to look through each item in our directory,
# only taking into consideration directories that
# contain the mcservice executable.
for item in sorted(os.listdir(SCRIPT_DIR)):

    # Get the path leading to mcservice.
    mcservicecmd = os.path.join(SCRIPT_DIR, item, "mcservice")

    # If this path happens to be a file, then assume
    # that the file is executable.
    if os.path.isfile(mcservicecmd):

        # Execute "mcservice status" and keep track of
        # the output for the corresponding version.
        try:
            exit_code = 0
            mcservice_output = subprocess.check_output(
                [
                    mcservicecmd,
                    "status"
                ]
            )

        # Chances are that we're not going to get a nice,
        # neat error code of zero when we call this command,
        # so I am handling the exception here, grabbing the
        # output if necessary.
        except subprocess.CalledProcessError as ex:
            exit_code = ex.returncode
            mcservice_output = ex.output
            
        s = "{0}: [{1}] {2}".format(item, exit_code, mcservice_output)
        sys.stdout.write(s)
        
# This is also for neatness.
sys.stdout.write("\n")
