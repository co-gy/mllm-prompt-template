from PIL import Image
from string import Template as StringTemplate


try:
    from .prompt import Prompt
except ImportError:
    from prompt import Prompt


class Template(StringTemplate):
    def __init__(self, template: str):
        super().__init__(template)

    def __str__(self):
        return self.template

    def __repr__(self):
        return self.__str__()
    
    def substitute(self, mapping=None, /, **kws):
        if mapping is None:
            mapping = {}
        all_mapping = {**mapping, **kws}
        image_var = {}
        for k, v in all_mapping.items():
            if isinstance(v, Image.Image):
                image_var[k] = v
                all_mapping[k] = f"<<<Image({k}): ({v})>>>"
        prompt = Prompt(prompt=super().substitute(all_mapping), image_var=image_var)
        return prompt

    def safe_substitute(self, mapping=None, /, **kws):
        if mapping is None:
            mapping = {}
        all_mapping = {**mapping, **kws}
        image_var = {}
        for k, v in all_mapping.items():
            if isinstance(v, Image.Image):
                image_var[k] = v
                all_mapping[k] = f"<<<Image({k}): ({v})>>>"
        prompt = Prompt(prompt=super().substitute(all_mapping), image_var=image_var)
        return prompt