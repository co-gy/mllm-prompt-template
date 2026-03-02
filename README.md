# MLLM Prompt Template

A Python template library for Multimodal LLMs(MLLMs) that extends Python's `string.Template` to support image substitution in prompts.

## Installation

```bash
pip install mllm-prompt-template
```

## Usage

```python
from mllm_prompt_template import Template
from PIL import Image

# Create template with image placeholders
prompt_template = """
这个人是$name, 这是他的自拍照:
$img
$name很可爱对不对
"""

# Substitute text and image variables
prompt = Template(prompt_template).safe_substitute(
    name="co-gy",
    img=Image.open("photo.jpg")
)

# Convert to OpenAI-style message format
messages = prompt.to_messages()

# Call MLLM (example with OpenAI-compatible API)
import openai

client = openai.OpenAI(base_url="http://localhost:8000/v1", api_key="EMPTY")

response = client.chat.completions.create(
    model="Qwen3-VL-8B-Instruct",
    messages=messages,
    max_tokens=500
)

print(response.choices[0].message.content)
```

## API

- `Template(prompt_template: str)` - Create template
- `safe_substitute(**kwargs)` - Substitute variables (supports strings and PIL Images)
- `to_messages()` - Convert to OpenAI-style message format

## Requirements

- Python >= 3.8
- Pillow >= 9.0.0

## License

MIT License
