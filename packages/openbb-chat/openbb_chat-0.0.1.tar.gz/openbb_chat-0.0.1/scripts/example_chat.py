from rich.progress import track
from typing import List
import pandas as pd
from openbb_chat.classifiers.stransformer import STransformerZeroshotClassifier
from openbb_chat.llms.guidance_wrapper import GuidanceWrapper
import argparse
from openbb_terminal.sdk import openbb

import torch

def parse_args(args=None):
    parser = argparse.ArgumentParser("Retrieve most similar description given an instruction.")
    parser.add_argument("-kc", "--keys-csv", type=str, required=True,
        help="Input .csv with pairs of descriptions and Python definitions. Columns should be 'Descriptions' and 'Definitions'.")
    parser.add_argument("-q", "--query", type=str, required=True,
        help="Sentence to use as query of the descriptions.")
    parser.add_argument("-cm", "--classifier-model", type=str, default="sentence-transformers/all-MiniLM-L6-v2",
        help="HF MNLI model to use. Default: sentence-transformers/all-MiniLM-L6-v2")
    parser.add_argument("-llm", "--large-language-model", type=str, default="openlm-research/open_llama_3b_v2",
        help="HF LLM model to use. Default: openlm-research/open_llama_3b_v2")
    parser.add_argument("-s", "--separator", type=str, default="@",
        help="Separator in .csv. Default: @.")
    return parser.parse_args(args=args)

def get_func_parameter_names(func_def: str) -> List[str]:
    # E.g. stocks(symbol: str, time: int) would be ["symbol", "time"]
    inner_func = func_def[func_def.index("(")+1:func_def.index(")")].strip()
    if inner_func == "":
        return []
    return [param.strip().split(":")[0].strip() for param in inner_func.split(",")]

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

    stranformer = STransformerZeroshotClassifier(args.classifier_model)
    key, _, idx = stranformer.classify(args.query, keys)
    print(key)

    func_def = definitions[idx]
    func_descr = descriptions[idx]

    param_names = get_func_parameter_names(func_def)
    if len(param_names) == 0:
        print("No parameters in the function.")
        exit(0)
    param_str = ""
    param_keys = [f"param_{idx}" for idx, _ in enumerate(param_names)]
    for idx, param in enumerate(param_names):
        param_str += f"{param}" + " = {{gen " + f"'{param_keys[idx]}'" + " stop='\n'}}\n"

    guidance_wrapper = GuidanceWrapper(model_id=args.large_language_model)
    template = f"""The Python function `{func_def}` is used to "{func_descr}". Given the prompt "{args.query}", write the correct parameters for the function using Python:
```python
{param_str[:-1]}
```"""
    program = guidance_wrapper(template)

    executed_program = program()
    
    inner_func_str = ",".join([executed_program[key] for key in param_keys])
    final_func_call = func_def[:func_def.index("(")+1] + inner_func_str + ")"
    print(f"{final_func_call=}")
    print(eval(final_func_call))

if __name__ == "__main__":
    main(parse_args())
