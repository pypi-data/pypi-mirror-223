from openbb_chat.llms.guidance_wrapper import GuidanceWrapper

guidance_wrapper = GuidanceWrapper()

program = guidance_wrapper("""The Python function openbb.stocks.ba.snews(symbol: str) is used to "Get headlines sentiment using VADER model over time".
Given the prompt "What is the headlines sentiment of Telefonica?", write the correct parameters for the function using Python:
```python
# symbol is the ticker of the company
symbol = {{gen 'out' stop='\n'}}
```""")

print(executed_program["out"])