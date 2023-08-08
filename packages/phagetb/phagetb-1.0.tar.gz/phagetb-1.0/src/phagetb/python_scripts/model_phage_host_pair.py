#################################################################
# This module contains the model class and the functions to run #
# The model to predict whether given phage host pair interacts  #
# or not based on sequences of the phage and bacteria           #
#################################################################

import warnings
warnings.filterwarnings('ignore')
import pickle as pkl
import pandas as pd
import numpy as np
import os
from Bio.Blast.Applications import NcbiblastnCommandline
import Bio
from Bio import SeqIO
import argparse
import shutil
from phagetb.python_scripts.model import *
import zipfile
import platform

nf_path = os.path.dirname(__file__)
temp_path = nf_path + '/../tmp'
base_path = nf_path + '/../base'

BLAST_BINARIES = {
    "Linux": "/../blast_binaries/linux/blastn",
    "Darwin": "/../blast_binaries/mac/blastn",
    "Windows": "/../blast_binaries/windows/blastn.exe",
}

def get_blastn_path(def_file_path):
    operating_system = platform.system()
    blastn_path = def_file_path + BLAST_BINARIES.get(operating_system)
    if not blastn_path:
        print(f"Unsupported operating system: {operating_system}")
        return None

    if not os.path.exists(blastn_path):
        print(f"BLASTN binary not found: {blastn_path}")
        return None

    return blastn_path

blastn_path = get_blastn_path(nf_path)

  #=======================================Phage , Host and Crisper Database Download===========================
if os.path.isdir('blastdb') == False:
        urllib.request.urlretrieve("https://webs.iiitd.edu.in/raghava/phagetb/downloads/blastdb_and_genome.zip","blastdb_and_genome.zip")
        with zipfile.ZipFile('./blastdb_and_genome.zip', 'r') as zip_ref:
            zip_ref.extractall('.')
            os.remove('./blastdb_and_genome.zip')
else:
        pass
blastdb_path = "blastdb"

def readFasta(fasta_file):
    """
    Convert fasta file to list of tuples
    """
    fasta_list = []
    for record in SeqIO.parse(fasta_file, "fasta"):
        fasta_list.append([record.id, record.description, record.seq.lower()])
    return fasta_list

def align_genome_sequences(seq1, seq2):
    '''
    Align two sequences using blastn
    '''
    if not os.path.exists(temp_path + "/temp"):
        os.makedirs(temp_path + "/temp")
    ran = np.random.randint(100, 100000)
    outfile = temp_path + "/temp/" + "/temp_" + str(ran) + ".csv"
    blastn_cline = NcbiblastnCommandline(cmd = blastn_path, query=seq1, subject=seq2, outfmt="6", out= outfile)
    stdout, stderr = blastn_cline()
    return outfile

def main():
    ## Read Arguments from command
    parser = argparse.ArgumentParser(description='Please provide following arguments') 
    parser.add_argument("-v", "--input_phage", type=str, required=True, help="Input: genome sequence of the phage in FASTA format or single sequence per line in single letter code")
    parser.add_argument("-b", "--intput_bacteria", type=str, required=True, help="Input: genome sequence of the bacteria in FASTA format or single sequence per line in single letter code")
    parser.add_argument("-o", "--output",type=str, help="Output: File for saving results by default outfile.csv")
    parser.add_argument("-l", "--levels", type=int, nargs='+', default=[1,2,3,4], help="Levels: 1: Blast against phage reference DB, 2: Blast against host reference DB, 3: Integrated model, 4: CRISPR")
    parser.add_argument("-t", "--threshold", type=float, default=0.01,help="Threshold: evalue threshold for similarity score")
    args = parser.parse_args()
    if args.output:
        outfile = args.output
    else:
        ran = np.random.randint(100, 100000)
        outfile = temp_path + '/output/outfile' + str(ran) + '.csv'
    try:
        check_levels(args.levels)
        levels = args.levels

    except Exception as e:
        print(e)
        print("Please provide valid levels")
        exit()

    input_file = args.input_phage
    input_bacteria = args.intput_bacteria
    threshold = args.threshold
    model = HierarchicalModel(args.levels)
    res = model.predict(input_file)
    try:
        host_id = res['Host']
        hosts = read_pickle_file(base_path + '/extras/hosts_list.pkl')
        ref_host = hosts[host_id] + '.fasta'
        ref_host_seq =  "genome_data/" + ref_host
        out = align_genome_sequences(input_bacteria, ref_host_seq)
        res = pd.read_csv(out, sep='\t')
        res.columns = ['qseqid', 'sseqid', 'pident', 'length', 'mismatch', 'gapopen', 'qstart', 'qend', 'sstart', 'send', 'evalue', 'bitscore']
        evalue = res['evalue'].min()

        df = pd.DataFrame()
        input_phage_name = "".join(os.path.split(input_file)[1].split('.')[:-1])
        df['Phage'] = [input_phage_name]
        input_bacteria_name = ".".join(os.path.split(input_bacteria)[1].split('.')[:-1])
        df['Input Host'] = [input_bacteria_name]
        df['Predicted Host'] = [hosts[host_id]]
        df['e-value of Alignment'] = [evalue]
        df['Interaction'] = 1 if evalue < threshold else 0
        df.to_csv(outfile, index=False)
        os.remove(out)
    except:
        df = pd.DataFrame()
        input_phage_name = "".join(os.path.split(input_file)[1].split('.')[:-1])
        df['Phage'] = [input_phage_name]
        input_bacteria_name = ".".join(os.path.split(input_bacteria)[1].split('.')[:-1])
        df['Input Host'] = [input_bacteria_name]
        df['Predicted Host'] = ["No Prediction Found"]
        df['e-value of Alignment'] = ["NA"]
        df['Interaction'] = ["NA"]
        df.to_csv(outfile, index=False)
        print("No prediction found")
    ## clean up
if __name__ == "__main__":
    main()


