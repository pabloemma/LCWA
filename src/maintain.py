# checks for system maintenance
# written ak March 2024

# define only imports, which are part of regular python3 distro
import importlib as IL
import sys
import subprocess

class Maintain():


    def __init__(self, mylist = None):

        """ this helps maintaining the speedtest server"""

        if(mylist != None):

            for package in mylist:
                result = self.CheckImport(package)
    




    def CheckImport(self,package=None):

        """ Checks if package is installed , if not installs package"""
        if(package == None):
            print('you need to give a package, exiting')
            sys.exit(0)
      
        if(IL.util.find_spec('package') is None):
            print('package {} is not installed, will try to install'.format(package))
            # implement pip as a subprocess:
            try:
                subprocess.check_call([sys.executable, '-m', 'pip', 'install', package])
                return True
            except:
                print('package {} cannot be installed'.format(package))
                return False

        
        else:
            print('package {} is installed'.format(package))
            return True
        



if __name__ == '__main__':
    import_list = ('tarfile','dropbox',\
                   'socket','ntplib',\
                   'inspect','json','loguru',
                   'matplotlib','textwrap')
    MA = Maintain(mylist = import_list)
    
    #MA.CheckImport(package = 'matplotlib1')

    