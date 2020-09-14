import tkinter 
from tkinter import messagebox
from tkinter import filedialog
import os
import sys
import platform
import subprocess

app = tkinter.Tk()
app.title("App")
app.geometry('700x500+200+200')
lbl=tkinter.Label(app, text="")
#This variable stores the information of the operating system.
o_sys=platform.system()

def retrieve_SRR():
    '''
    This function recieves an SRR accession number and with string methods creates the ftp url where the file is,
    and dowloads it. It uses different methods depending on the operating system.
    ''' 
    lbl.config(text="Downloading your selected fastq.gz file.")
    SRR = text_Widget.get("1.0",'end-1c')
    first_digits=SRR[0:6]
    last_digits='00'+SRR[-1:]
    ftp_link='ftp://ftp.sra.ebi.ac.uk/vol1/fastq/'+first_digits+'/'+last_digits+'/'+SRR+'/'+SRR+'.fastq.gz'
    if 'Linux' in o_sys:
        os.system('cd ../')
        os.system('wget '+ftp_link)
    elif 'Windows' in o_sys:
        os.system('cd ../')
        os.system('curl.exe -O '+ftp_link)
    lbl.config(text="Done!")


def unTar():
    '''
    This function untars the SRR file previously downloaded and deletes it, keeping only the .fastq file.
    '''
    lbl.config(text="Extracting the fastq file. This takes a while and freezes the app, don't close it!")
    SRR= text_Widget.get("1.0",'end-1c')
    if 'Linux' in o_sys:
        os.system('gunzip '+SRR+'.fastq.gz')
        os.system('rm '+SRR+'.fastq.gz')
    elif 'Windows' in o_sys:
        os.system('gzip -d '+SRR+'.fastq.gz')
        os.system('del '+SRR+'.fastq.gz')
    lbl.config(text="Done!")

def download_Genome():
    '''
    This function calls the scripts to download the Human genome and move the files where they need to be.
    '''
    lbl.config(text="Downloading and extracting reference genome. This takes a while and freezes the app, don't close it!")
    if 'Linux' in o_sys:
        os.system('bash download_genome_index.sh')
    elif 'Windows' in o_sys:
        subprocess.check_call(['wsl', 'python3','download_genome_index.py'])
    lbl.config(text="Done")

def install_programs():
    '''
    This function calls the script used to setup anaconda and the required packages.
    '''
    if 'Linux' in o_sys:
        print(os.system('bash anaconda_setup.sh'))
    if 'Windows' in o_sys:
        print(subprocess.check_call(['wsl', 'python3','anaconda_setup.py']))

def chooseDir():
    '''
    This function stores the directory where the samples are stored on a variable for later use.
    '''
    app.sourceFolder =  filedialog.askdirectory(parent=app, initialdir= "/home/", title='Please select a directory')
    app.sourceFolder=app.sourceFolder+'/'
    return


def chooseFile():
    '''
    This function stores in a variable the path to the file to analyze.
    '''
    app.sourceFile = filedialog.askopenfilename(parent=app, initialdir= "/home/", title='Please select a directory')
    app.sourceFile=app.sourceFile[app.sourceFile.find('SRR'):]
    return

def calculate():
    '''
    This function calls the pipeline :)
    '''
    lbl.config(text="Starting the pipeline.")
    lbl.config(text="Cheking for missing modules and installing them if missing.")
    os.system('python3 modules.py')
    lbl.config(text="Done.")
    lbl.config(text="Starting the whole genome alignment. This takes time.")
    if 'Linux' in o_sys:
        os.system('python3 Aln_WG.py '+app.sourceFile+' '+app.sourceFolder)
        lbl.config(text="Done!")
        lbl.config(text="Aligning versus the mature genome.")
        os.system('python3 Aln_MG.py '+app.sourceFile)
        lbl.config(text="Done!")
        lbl.config(text="Aligning versus the precursor genome.")
        os.system('python3 Aln_PG.py '+app.sourceFile)
        lbl.config(text="Done!")
        lbl.config(text="Aligning versus the mature genome with one mismatch in the seed.")
        os.system('python3 Aln_M1G.py '+app.sourceFile)
        lbl.config(text="Done!")
        lbl.config(text="Obtaining the final counts.")
        os.system('python3 Obtain_counts.py '+app.sourceFile)
        lbl.config(text="Done!")
        lbl.config(text="Doing the pileup.")
        os.system('python3 pileup_ok.py '+app.sourceFile)
        lbl.config(text="Done!")
    if 'Windows' in o_sys:
        subprocess.check_call(['wsl','python3', 'Aln_WG.py ',app.sourceFile,' ', app.sourceFolder])
        lbl.config(text="Done!")
        lbl.config(text="Aligning versus the mature genome.")
        subprocess.check_call(['wsl','python3', 'Aln_MG.py ',app.sourceFile])
        lbl.config(text="Done!")
        lbl.config(text="Aligning versus the precursor genome.")
        subprocess.check_call(['wsl','python3', 'Aln_PG.py ',app.sourceFile])
        lbl.config(text="Done!")
        lbl.config(text="Aligning versus the mature genome with one mismatch in the seed.")
        subprocess.check_call(['wsl','python3', 'Aln_M1G.py ',app.sourceFile])
        lbl.config(text="Done!")
        lbl.config(text="Obtaining the final counts.")
        subprocess.check_call(['wsl','python3', 'Obtain_counts.py ',app.sourceFile])
        lbl.config(text="Done!")
        lbl.config(text="Doing the pileup.")
        subprocess.check_call(['wsl','python3','pileup_ok.py ',app.sourceFile])
        lbl.config(text="Done!")

def r_preparation():
    '''
    This script takes all the counts step result files and joins them in a single file in order to analyse them in R
    '''
    os.system('python3 join_results.py')
def r_script():
    '''
    This function launches an R script aimed at doing a differential expression anlysis of the results obtained from the pipeline
    '''
    if 'Linux' in o_sys:
        subprocess.call(["/usr/bin/Rscript", "--vanilla", "DEG_analysis.r"])
    if 'Windows' in o_sys:
        print('In order to run th DEG analysis in windows, close the GUI and write the following code into the console:')
        print('Rscript DEG_analysis.r')
lbl.pack()

text_Widget=tkinter.Text(app, height=1, width=30)
text_Widget.place(x=50, y=50)

download_Button=tkinter.Button(app, text='Download', width=20, height=1, command=retrieve_SRR)
download_Button.place(x=300, y=50)

untar_Button = tkinter.Button(app, text="Untar and delete .gz file", command= unTar)
untar_Button.place(x=490, y=50)

genome_Button=tkinter.Button(app, text='Download Genome', width=20, height=1, command=download_Genome)
genome_Button.place(x=155, y=125)

programs_Button=tkinter.Button(app, text='Download programs', width=20, height=1, command=install_programs)
programs_Button.place(x=350, y=125)

app.sourceFolder = ''
b_chooseDir = tkinter.Button(app, text = "Chose Folder", width = 20, height = 3, command = chooseDir)
b_chooseDir.place(x = 155,y = 200)
b_chooseDir.width = 100

app.sourceFile = ''
b_chooseFile = tkinter.Button(app, text = "Chose File", width = 20, height = 3, command = chooseFile)
b_chooseFile.place(x = 350,y = 200)
b_chooseFile.width = 100

r_button=tkinter.Button(app, text="DEG analysis with R", width=20, height=3, command=r_script)
r_button.pack(side='bottom', padx=15, pady=15)

r_prep=tkinter.Button(app, text="Join results for R", width=20, height=1, command=r_preparation)
r_prep.pack(side='bottom', padx=15, pady=15)

submit_button = tkinter.Button(app, text="Submit", width = 20, height = 3, command=calculate)
submit_button.pack(side='bottom', padx=15, pady=15)

app.mainloop()
