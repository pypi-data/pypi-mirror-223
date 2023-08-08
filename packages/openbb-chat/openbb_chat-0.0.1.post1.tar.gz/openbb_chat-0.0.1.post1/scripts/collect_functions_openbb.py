import argparse
import os
import re
import glob
import subprocess
import pandas as pd
import csv
from multiprocessing import Pool
from functools import partial

from tqdm import tqdm

def parse_args(args=None):
    parser = argparse.ArgumentParser("Retrieve Python functions from OpenBB docs")
    parser.add_argument("-i", "--in_folder", type=str, required=True,
        help="Input folder to recursively for .md documentation files")
    parser.add_argument("-o", "--out_csv", type=str, required=True,
        help="Output .csv file to store retrieved functions and their descriptions")
    parser.add_argument("-p", "--num_processes", type=int, default=8,
        help="No. processes to use. (Default: 8)")
    return parser.parse_args(args=args)

def get_function_and_descr_from_md(infile: str) -> None:
    with open(infile, "r") as f:
        text_md = f.read()
    functions_descr = [x[0] for x in re.findall(r'([A-Z].*)\.?\s*(\[.+\])?\s+Source Code', text_md)]
    functions_def = re.findall(r'openbb\.[\w\.?]+\(.*\)', text_md)

    if len(functions_descr) == 0 or len(functions_def) == 0:
        return "", ""
    return functions_descr[0], functions_def[0]

def main(args):
    doc_files = glob.glob(os.path.join(args.in_folder, "**/*.md"), recursive=True)

    function_descrs = []
    function_defs = []
    with Pool(processes=args.num_processes) as p:
        with tqdm(total=len(doc_files)) as pbar:
            for functions_descr, functions_def in p.imap_unordered(
                partial(get_function_and_descr_from_md), doc_files
            ):
                if functions_descr != "":
                    function_descrs.append(functions_descr)
                if functions_def != "":
                    function_defs.append(functions_def) 
                pbar.update()

    df = pd.DataFrame()
    df["Descriptions"] = function_descrs
    df["Definitions"] = function_defs
    df.to_csv(args.out_csv, sep="@", quoting=csv.QUOTE_NONE, index=False)

if __name__ == "__main__":
    main(parse_args())