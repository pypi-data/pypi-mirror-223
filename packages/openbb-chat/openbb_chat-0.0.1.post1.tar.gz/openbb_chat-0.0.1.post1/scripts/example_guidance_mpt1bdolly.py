import os

import guidance
import torch
from transformers import AutoTokenizer, BitsAndBytesConfig, AutoModelForCausalLM

model_id = "mosaicml/mpt-1b-redpajama-200b-dolly"

tokenizer = AutoTokenizer.from_pretrained(model_id)

# set the default language model used to execute guidance programs
guidance.llm = guidance.llms.Transformers(
    model=model_id,
    tokenizer=tokenizer,
    device_map={"":0},
    torch_dtype=torch.bfloat16,
    trust_remote_code=True
)

# define a guidance program that adapts a proverb
program = guidance("""The Python function openbb.stocks.ba.snews(symbol: str), where symbol is the ticker of a company, is used to "Get headlines sentiment using VADER model over time".
Given the prompt "What is the headlines sentiment of Amazon?", write the correct parameters for the function using Python:
```python
symbol="{{gen 'out' temperature=0.8 top_p=0.8 stop='"'}}
openbb.stocks.ba.snews(symbol)
```""")

# execute the program on a specific proverb
executed_program = program()

print(executed_program["out"])