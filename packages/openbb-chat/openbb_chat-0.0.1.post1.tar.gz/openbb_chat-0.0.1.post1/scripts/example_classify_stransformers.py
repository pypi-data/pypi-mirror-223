from rich.progress import track
import pandas as pd
from openbb_chat.classifiers.stransformer import STransformerZeroshotClassifier
import argparse

import torch

def parse_args(args=None):
    parser = argparse.ArgumentParser("Retrieve most similar description given an instruction.")
    parser.add_argument("-kc", "--keys_csv", type=str, required=True,
        help="Input .csv with pairs of descriptions and Python definitions. Columns should be 'Descriptions' and 'Definitions'.")
    parser.add_argument("-q", "--query", type=str, required=True,
        help="Sentence to use as query of the descriptions.")
    parser.add_argument("-m", "--model", type=str, default="sentence-transformers/all-MiniLM-L6-v2",
        help="HF MNLI model to use. Default: sentence-transformers/all-MiniLM-L6-v2")
    parser.add_argument("-s", "--separator", type=str, default="@",
        help="Separator in .csv. Default: @.")
    parser.add_argument("-e", "--export", type=str,
        help=".csv file to export descriptions and their score.")
    return parser.parse_args(args=args)

@torch.inference_mode()
def main(args):
    df = pd.read_csv(args.keys_csv, sep=args.separator)
    df = df.dropna()
    descriptions = df["Descriptions"].tolist()
    definitions = df["Definitions"].tolist()

    keys = []
    for idx, descr in track(enumerate(descriptions), total=len(descriptions), description="Processing..."):
        topics = definitions[idx][:definitions[idx].index("(")].split(".")[1:]
        if descr.find("[") != -1:
            descr = descr[:descr.find("[")].strip()
        if descr.strip()[-1] != ".":
            search_str = f"{descr.strip()}. Topics: {', '.join(topics)}."
        else:
            search_str = f"{descr.strip()} Topics: {', '.join(topics)}."
        keys.append(search_str)

    stranformer = STransformerZeroshotClassifier(args.model)
    key, score, _ = stranformer.classify(args.query, keys)

    print(key, score)

if __name__ == "__main__":
    main(parse_args())
