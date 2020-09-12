import os

def import_or_install(package):
    '''
    This function will import or install a package. If they are found in the system, they will be imported
    If not, they will be installed
    '''
    try:
        __import__(package)
    except ImportError:
        os.system('pip install '+package)    

#This is the list of the packages needed, imported or installed
packages=['argparse','subprocess','sys','glob','pysam','re']

#Calling the function for a iterative list of packages
for i_package in packages:
    import_or_install(i_package)