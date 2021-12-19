#imports package in case they are missing
# for python3

import subprocess
import sys

def InstallPackage(package):
    subprocess.check_call([sys.executable, "-m", "pip", "install","iperf3"])