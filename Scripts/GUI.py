import tkinter 
from tkinter import messagebox
from tkinter import filedialog
from tkinter import ttk
import os
import sys
import platform
import subprocess

app = tkinter.Tk()
app.title("App")
app.geometry('700x600+200+200')
tab_parent = ttk.Notebook(app)
tab1 = ttk.Frame(tab_parent)
tab2 = ttk.Frame(tab_parent)
tab_parent.add(tab1, text="Pipeline")
tab_parent.add(tab2, text="R analysis")
tab_parent.pack(expand=1, fill='both')
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
    if 'Linux' in o_sys or 'Darwin' in o_sys:
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
    if 'Linux' in o_sys or 'Darwin' in o_sys:
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
    if 'Linux' in o_sys or 'Darwin' in o_sys:
        os.system('bash download_genome_index.sh')
    elif 'Windows' in o_sys:
        subprocess.check_call(['wsl', 'python3','download_genome_index.py'])
    lbl.config(text="Done")

def install_programs():
    '''
    This function calls the script used to setup anaconda and the required packages.
    '''
    if 'Linux' in o_sys or 'Darwin' in o_sys:
        print(os.system('bash anaconda_setup.sh'))
    elif 'Windows' in o_sys:
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

######new functions
def chooseGroup1():
    i=0
    files_list=os.listdir(app.sourceFolder)
    for files in files_list:
        app.group1[i] = filedialog.askopenfilename(parent=app, initialdir= "/home/", title='Please select a directory')
        app.group1[i]=app.group1[i][app.group1[i].find('.fastq'):]
        i=i+1
    return

def chooseGroup2():
    i=0
    files_list=os.listdir(app.sourceFolder)
    for files in files_list:
        app.group2[i] = filedialog.askopenfilename(parent=app, initialdir= "/home/", title='Please select a directory')
        app.group2[i]=app.group2[i][app.group2[i].find('.fastq'):]
        i=i+1
    return

def rename_group1():
    for element in app.group1:
        element=name_group1+'_'+element
    with open('group1_names.txt', 'w') as f:
        for item in app.group1:
            f.write("%s\n" % item)
    return

def rename_group2():
    for element in app.group2:
        element=name_group2+'_'+element
    with open('group2_names.txt', 'w') as f:
        for item in app.group2:
            f.write("%s\n" % item)
    return

def countsAnalysis():
    if 'Linux' in o_sys or 'Darwin' in o_sys:
        subprocess.call(["/usr/bin/Rscript", "--vanilla", "PLOTS_Counts_Total.r"])
        subprocess.call(["/usr/bin/Rscript", "--vanilla", "PLOTS_Prop_Mature_Precursor.r"])
    elif 'Windows' in o_sys:
        print('In order to run th DEG analysis in windows, close the GUI and write the following code into the console:')
        print('Rscript PLOTS_Counts_Total.r')
        print('Rscript PLOTS_Prop_Mature_Precursor.r')

def modAnalysis():
    if 'Linux' in o_sys or 'Darwin' in o_sys:
        subprocess.call(["/usr/bin/Rscript", "--vanilla", "PLOTS_Modifications_Analisis.r"])
    elif 'Windows' in o_sys:
        print('In order to run th DEG analysis in windows, close the GUI and write the following code into the console:')
        print('Rscript PLOTS_Modifications_Analisis.r')

#######

def calculate():
    '''
    This function calls the pipeline :)
    '''
    lbl.config(text="Starting the pipeline.")
    lbl.config(text="Cheking for missing modules and installing them if missing.")
    os.system('python3 modules.py')
    lbl.config(text="Done.")
    lbl.config(text="Starting the whole genome alignment. This takes time.")
    if 'Linux' in o_sys or 'Darwin' in o_sys:
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
        os.system('python3 pileup_mod.py '+app.sourceFile)
        lbl.config(text="Done!")
    elif 'Windows' in o_sys:
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
        subprocess.check_call(['wsl','python3','pileup_mod.py ',app.sourceFile])
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
    if 'Linux' in o_sys or 'Darwin' in o_sys:
        subprocess.call(["/usr/bin/Rscript", "--vanilla", "DEG_analysis.r"])
        subprocess.call(["/usr/bin/Rscript", "--vanilla", "iso_test_all.r"])
    elif 'Windows' in o_sys:
        print('In order to run th DEG analysis in windows, close the GUI and write the following code into the console:')
        print('Rscript DEG_analysis.r')
        print('Rscript iso_test_all.r')
lbl.pack()

##WIDGETS FOR TAB PIPELINE##

text_Widget=tkinter.Text(tab1, height=1, width=30)
text_Widget.place(x=50, y=50)

download_Button=tkinter.Button(tab1, text='Download', width=20, height=1, command=retrieve_SRR)
download_Button.place(x=300, y=50)

untar_Button = tkinter.Button(tab1, text="Untar and delete .gz file", command= unTar)
untar_Button.place(x=490, y=50)

genome_Button=tkinter.Button(tab1, text='Download Genome', width=20, height=1, command=download_Genome)
genome_Button.place(x=155, y=125)

programs_Button=tkinter.Button(tab1, text='Download programs', width=20, height=1, command=install_programs)
programs_Button.place(x=350, y=125)

app.sourceFolder = ''
b_chooseDir = tkinter.Button(tab1, text = "Chose Folder", width = 20, height = 3, command = chooseDir)
b_chooseDir.place(x = 155,y = 200)
b_chooseDir.width = 100

app.sourceFile = ''
b_chooseFile = tkinter.Button(tab1, text = "Chose File", width = 20, height = 3, command = chooseFile)
b_chooseFile.place(x = 350,y = 200)
b_chooseFile.width = 100

r_button=tkinter.Button(tab1, text="DEG analysis with R", width=20, height=3, command=r_script)
r_button.pack(side='bottom', padx=15, pady=15)

r_prep=tkinter.Button(tab1, text="Join results for R", width=20, height=1, command=r_preparation)
r_prep.pack(side='bottom', padx=15, pady=15)

submit_button = tkinter.Button(tab1, text="Submit", width = 20, height = 3, command=calculate)
submit_button.pack(side='bottom', padx=15, pady=15)

##WIDGETS FOR TAB R ANALYSIS##

app.group1=[]
b_group1=tkinter.Button(tab2, text = "Group 1", width = 20, height = 3, command = chooseGroup1)
b_group1.place(x = 50,y = 50)
b_group1.width = 100

name_group1=tkinter.Text(tab2, height=1, width=25)
name_group1.place(x=50, y=150)

submit_1_Button=tkinter.Button(tab2, text='Submit', width=20, height=1, command=rename_group1)
submit_1_Button.place(x=50, y=200)

app.group2=[]
b_group2=tkinter.Button(tab2, text = "Group 2", width = 20, height = 3, command = chooseGroup1)
b_group2.place(x = 400,y = 50)
b_group2.width = 100

name_group2=tkinter.Text(tab2, height=1, width=25)
name_group2.place(x=400, y=150)

submit_2_Button=tkinter.Button(tab2, text='Submit', width=20, height=1, command=rename_group2)
submit_2_Button.place(x=400, y=200)

b_countsAnalysis=tkinter.Button(tab2, text='Counts analysis', width=20, height=3, command=countsAnalysis)
b_countsAnalysis.place(x=50, y= 300)
b_countsAnalysis.width=100

b_modAnalysis=tkinter.Button(tab2, text='Modifications analysis', width=20, height=3, command=modAnalysis)
b_modAnalysis.place(x=400, y= 300)
b_modAnalysis.width=100


app.mainloop()
