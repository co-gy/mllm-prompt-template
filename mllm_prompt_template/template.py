from PIL import Image
from string import Template as StringTemplate
from io import BytesIO
import base64
import re


class Template:
    def __init__(self, prompt_template: str):
        self.prompt_template: StringTemplate = StringTemplate(prompt_template)
        self.prompt: str = self.prompt_template.safe_substitute()
        self.text_var = {}
        self.image_var = {}


    def __str__(self):
        return self.prompt

    def __repr__(self):
        return self.prompt
        
    def safe_substitute(self, **kwargs) -> str:
        for k, v in kwargs.items():
            if isinstance(v, Image.Image):
                self.image_var[k] = v
                self.prompt = StringTemplate(self.prompt).safe_substitute(**{k: f"<<<Image({k}): {v}>>>"})
            else:
                self.text_var[k] = f"{v}"
                self.prompt = StringTemplate(self.prompt).safe_substitute(**{k: v})
        return self
    
    def to_messages(self):
        messages = [{
            "role": "user",
            "content": []
        }]
        
        separate = re.split(r"(<<<Image\(.*?\): .*?>>>)", self.prompt)
        for item in separate:
            match = re.match(r"<<<Image\((.*?)\): .*?>>>", item)
            if match is not None:
                img_name = match.group(1)
                img = self.image_var[img_name]
                img_base64 = self.img2base64(img)
                messages[0]["content"].append({
                    "type": "image_url",
                    "image_url": {
                        "url": img_base64
                    }
                })
            else:
                messages[0]["content"].append({
                    "type": "text",
                    "text": item
                })
        return messages

    @staticmethod
    def img2base64(img: Image.Image) -> str:
        img_buffer = BytesIO()
        if img.mode == 'RGBA':
            img = img.convert('RGB')
        img.save(img_buffer, format="JPEG")
        img_byte = img_buffer.getvalue()
        img_base64 = base64.b64encode(img_byte).decode('utf-8')
        return f'data:image/jpeg;base64,' + img_base64