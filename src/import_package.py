#imports package in case they are missing
# for python3

import subprocess
import sys

def InstallPackage(package ):
    # checks if program is installed, if not will try it with piup

    try:
        import package

    except ImportError:
        print('will try to install ',package)
        subprocess.check_call([sys.executable, "-m", "pip", "install","iperf3"])
    
    else:
        print('package  ', package, '  is already installed')

if __name__ == "__main__":
    InstallPackage('ntplib')
