import os

def import_or_install(package):
    try:
        __import__(package)
    except ImportError:
        os.system('pip install '+package)    

packages=['argparse','subprocess','sys','glob','pysam','re']

for i_package in packages:
    import_or_install(i_package)