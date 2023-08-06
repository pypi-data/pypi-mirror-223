import sys
import os
import platform
import subprocess
import zipfile 
import tarfile
import logging
from urllib import request 
# Set the log level by environment variable, default is INFO.
LOGLEVEL = os.environ.get('PY_VULCAN_LOGLEVEL', 'INFO').upper()
logging.basicConfig(level=LOGLEVEL)

EXECUTABLE_SOURCE_URL = 'https://github.com/Canner/vulcan-sql/releases/latest/download/'

# The executable file name for different system.
EXECUTABLE_FILES = {
    "Windows": "vulcan.win.zip",
    "Linux": "vulcan.linux.tar.gz",
    "Darwin": "vulcan.osx.tar.gz",
}


def run_vulcan():
    system = platform.system()
    supported_systems = ["Linux", "Darwin", "Windows"]

    if system not in supported_systems:
        logging.info("Not supported to run vulcan on '{}'.".format(system))
        exit("Install failed, current only support {}...".format(supported_systems))
    try:
        args = ''.join(sys.argv[1:])
        logging.debug("start to download executable file...")
        # get the file url source location
        executable_file_url = EXECUTABLE_SOURCE_URL + EXECUTABLE_FILES[system]
        logging.debug("executable file url: {}".format(executable_file_url))
        # download the executable file and save it to current directory by filename provided from EXECUTABLE_FILES[system].
        request.urlretrieve(executable_file_url, EXECUTABLE_FILES[system])
        # Run the executable file.
        if system == "Windows":
            with zipfile.ZipFile(EXECUTABLE_FILES[system], 'r') as zf:
                zf.extractall()
                subprocess.call("vulcan.exe {}".format(args), shell=True)
                subprocess.call("del vulcan.exe", shell=True)
            subprocess.call("del {}".format(EXECUTABLE_FILES[system]), shell=True)
        else:
            with tarfile.open(EXECUTABLE_FILES[system], 'r:gz') as tar:
                tar.extractall()
                subprocess.call("./vulcan {}".format(args), shell=True)
                subprocess.call("rm vulcan", shell=True)
            subprocess.call("rm {}".format(EXECUTABLE_FILES[system]), shell=True)
    except Exception as e:
        raise SystemExit(e)

