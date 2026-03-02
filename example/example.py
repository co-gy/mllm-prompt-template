from mllm_prompt_template.template import Template
from example.mllm import MLLM, LLM

from PIL import Image



mllm = LLM(base_url="http://localhost:8000/v1", api_key="EMPTY", model="Qwen3-VL-8B-Instruct")

prompt_kuakua = """
这个人是$name, 这是他的自拍照:
$img
$name很可爱对不对, 具体描述一下ta头发的颜色, 并夸夸ta
"""

prompt = Template(prompt_kuakua).safe_substitute(name="co-gy", img=Image.open('img.jpg'))
messages = prompt.to_messages()
response = mllm(messages)
print(response)