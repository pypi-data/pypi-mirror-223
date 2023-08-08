import os

import guidance
import torch
from transformers import AutoTokenizer, BitsAndBytesConfig, AutoModelForCausalLM

model_id = "meta-llama/Llama-2-7b-chat-hf"

tokenizer = AutoTokenizer.from_pretrained(model_id)

bnb_config = BitsAndBytesConfig(
    load_in_4bit=True,
    bnb_4bit_use_double_quant=True,
    bnb_4bit_quant_type="nf4",
    bnb_4bit_compute_dtype=torch.bfloat16
)

# set the default language model used to execute guidance programs
guidance.llm = guidance.llms.Transformers(
    model=model_id,
    tokenizer=tokenizer,
    device_map="auto", # offloads if needed
    quantization_config=bnb_config,
    trust_remote_code=True,
    token=os.environ["HF_AUTH_TOKEN"]
)

# define a guidance program that adapts a proverb
program = guidance("""Tweak this proverb to apply to model instructions instead.

{{proverb}}
- {{book}} {{chapter}}:{{verse}}

UPDATED
Where there is no guidance{{gen 'rewrite' stop="\\n-"}}
- GPT {{#select 'chapter'}}9{{or}}10{{or}}11{{/select}}:{{gen 'verse'}}""")

# execute the program on a specific proverb
executed_program = program(
    proverb="Where there is no guidance, a people falls,\nbut in an abundance of counselors there is safety.",
    book="Proverbs",
    chapter=11,
    verse=14
)