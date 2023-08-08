from transformers import AutoTokenizer, RobertaModel
import pandas as pd
from rich.progress import track
import argparse

import torch

def parse_args(args=None):
    parser = argparse.ArgumentParser("Retrieve most similar description given an instruction.")
    parser.add_argument("-kc", "--keys_csv", type=str, required=True,
        help="Input .csv with pairs of descriptions and Python definitions. Columns should be 'Descriptions' and 'Definitions'.")
    parser.add_argument("-q", "--query", type=str, required=True,
        help="Sentence to use as query of the descriptions.")
    parser.add_argument("-m", "--model", type=str, default="roberta-base",
        help="HF model to use. Default: roberta-base")
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

    tokenizer = AutoTokenizer.from_pretrained(args.model)

    model = RobertaModel.from_pretrained(args.model)
    model.eval()

    inputs = tokenizer(args.query, return_tensors="pt")

    target_embed = model(**inputs).pooler_output

    max_cosine_sim = -1 # min. possible cosine similarity
    most_sim_descr = ""
    if args.export is not None:
        cosine_sims = []
        descrs = []
    for idx, descr in track(enumerate(descriptions), total=len(descriptions), description="Processing..."):
        topics = definitions[idx][:definitions[idx].index("(")].split(".")[1:]
        if descr.find("[") != -1:
            descr = descr[:descr.find("[")].strip()
        if descr.strip()[-1] != ".":
            search_str = f"{descr.strip()}. Topics: {', '.join(topics)}."
        else:
            search_str = f"{descr.strip()} Topics: {', '.join(topics)}."
        inputs = tokenizer(search_str, return_tensors="pt")
        descr_embed = model(**inputs).pooler_output

        cosine_sim = torch.sum(
            torch.nn.functional.normalize(target_embed) * torch.nn.functional.normalize(descr_embed)
        )
        if cosine_sim > max_cosine_sim:
            most_sim_descr = descr
            max_cosine_sim = cosine_sim
        if args.export is not None:
            cosine_sims.append(cosine_sim.cpu().numpy())
            descrs.append(descr)

    print(most_sim_descr, max_cosine_sim)
    if args.export is not None:
        export_df = pd.DataFrame()
        export_df["Descriptions"] = descrs
        export_df["Scores"] = cosine_sims
        export_df.to_csv(args.export, index=False)

if __name__ == "__main__":
    main(parse_args())
