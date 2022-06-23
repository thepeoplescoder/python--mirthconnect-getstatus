#!/usr/bin/env python
#
# This script is used to get the status of each installed
# instance of Mirth Connect on my machine.
#
# 12/7/2015 by Austin Cathey
#
# Updates:
#    6/22/2022
#        This code properly runs on Python 2 and 3!

from __future__ import print_function
from __future__ import unicode_literals

# Imports
import os
import sys
import subprocess

# Get the directory in which this script resides.
# The requirement is that this script must exist in
# the same directory as all of the instances of Mirth
# Connect that you wish to run.
SCRIPT_DIR = os.path.dirname(os.path.realpath(__file__))

# main_nt #################################################
def main_nt(argv):
    """This approach is pretty lazy and I need to fix it later."""
    import socket

    try:
        import requests
        requests.packages.urllib3.disable_warnings()
    except ImportError:
        sys.exit("Please run: pip install --user requests")

    # A few constants
    SOCKET_ADDRESS = ("localhost", 8443)
    SOCKET_ADDRESS_STR = ":".join(map(str, SOCKET_ADDRESS))
    AUTH_CREDENTIALS = ("admin", "admin")

    # this does what you think it does
    # and reads how you think it would read
    def socket_is_not_open_at(address):
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        try:
            return sock.connect_ex(address)
        finally:
            sock.close()

    # leave if socket not open
    if socket_is_not_open_at(SOCKET_ADDRESS):
        sys.exit("{0} is not open".format(SOCKET_ADDRESS_STR))

    # what version of MC are we running?
    mc_version = requests.get("https://{0}/api/server/version".format(SOCKET_ADDRESS_STR),
        auth=AUTH_CREDENTIALS,
        headers={
            "X-Requested-With": "some python script I wrote",
        },
        verify=False).text

    # display it
    print("Mirth Connect {0} is running.".format(mc_version))

    # we're done.
    return 0

# main_default ############################################
def main_default(argv):
    command = {"executable": "mcservice", "flags": ["status"]}

    # Here we're going to populate the statuses variable.
    #
    # We need to look through each item in our directory,
    # only taking into consideration directories that
    # contain the mcservice executable.
    for item in sorted(os.listdir(SCRIPT_DIR)):

        # Get the path leading to mcservice.
        mcservicecmd = os.path.join(SCRIPT_DIR, item, command["executable"])

        # If this path happens to be a file, then assume
        # that the file is executable.
        if os.path.isfile(mcservicecmd):

            # Execute "mcservice status" and keep track of
            # the output for the corresponding version.
            try:
                exit_code = 0

                # we can safely assume the previously set
                # exit code of zero if this line executes
                # successfully.
                mcservice_output = subprocess.check_output(
                    [mcservicecmd] + command["flags"],
                    stderr=subprocess.STDOUT)

            # Chances are that we're not going to get a nice,
            # neat error code of zero when we call this command,
            # so I am handling the exception here, grabbing the
            # output if necessary.
            except subprocess.CalledProcessError as ex:
                exit_code = ex.returncode
                mcservice_output = ex.output
                
            s = "{0}: [{1}] {2}".format(item, exit_code, mcservice_output.decode("utf-8"))
            s = s.replace(os.linesep, " ")
            s = s.strip()

            print(s)

    return 0

if __name__ == "__main__":
    main = {"nt": main_nt}
    sys.exit(main.get(os.name, main_default)(sys.argv))