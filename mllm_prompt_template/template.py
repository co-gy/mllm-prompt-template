from PIL import Image
from string import Template as StringTemplate
from textwrap import shorten
from io import BytesIO
import base64
import re


class Template(StringTemplate):
    def __init__(self, template: str):
        super().__init__(template)
        self.prompt = template
        self.text_var = {}
        self.image_var = {}

    def __str__(self):
        template = shorten(self.template, 30)
        all_var = {**self.text_var, **self.image_var}
        var_str = ", ".join([f"{var}={shorten(str(all_var.get(var, f'${var}')), 30)}" for var in self.get_identifiers()])
        return f"Template('{template}'|{var_str})"

    def __repr__(self):
        return f"Template('{shorten(self.template, 30)}')"
    
    def substitute(self, mapping=None, /, **kws):
        if mapping is None:
            mapping = {}
        all_mapping = {**mapping, **kws}
        for k, v in all_mapping.items():
            if isinstance(v, Image.Image):
                self.image_var[k] = v
                all_mapping[k] = f"<<<Image({k}): {v}>>>"
            else:
                self.text_var[k] = f"{v}"
        self.prompt = super().substitute(all_mapping)
        return self.prompt

    def safe_substitute(self, mapping=None, /, **kws):
        if mapping is None:
            mapping = {}
        all_mapping = {**mapping, **kws}
        for k, v in all_mapping.items():
            if isinstance(v, Image.Image):
                self.image_var[k] = v
                all_mapping[k] = f"<<<Image({k}): {v}>>>"
            else:
                self.text_var[k] = f"{v}"
        self.prompt = super().safe_substitute(all_mapping)
        return self.prompt
    
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