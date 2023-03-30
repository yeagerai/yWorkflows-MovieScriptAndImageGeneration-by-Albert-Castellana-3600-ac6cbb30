
import os
from typing import Optional

import yaml
from dotenv import load_dotenv
from fastapi import FastAPI
from pydantic import BaseModel
import openai

from core.abstract_component import AbstractComponent


class GPT4ScriptGeneratorInputDict(BaseModel):
    theme_text: str


class GPT4ScriptGeneratorOutputDict(BaseModel):
    theme_text: str
    script_text: str
    component_internal_status: int

class GPT4ScriptGenerator(AbstractComponent):
    def __init__(self) -> None:
        super().__init__()
        with open(self.component_configuration_path(), "r", encoding="utf-8") as file:
            yaml_data = yaml.safe_load(file)
        self.api_key: Optional[str] = os.environ.get(
            yaml_data["parameters"]["api_key"]
        )
        self.model_configuration: str = yaml_data["parameters"]["model_configuration"]

    def transform(
        self, args: GPT4ScriptGeneratorInputDict
    ) -> GPT4ScriptGeneratorOutputDict:

        openai.api_key = self.api_key
        theme_text = args.theme_text
        model_configuration = self.model_configuration

        prompt = {"text": theme_text, "configuration": model_configuration}

        try:
            response = openai.Completion.create(prompt=prompt)
            generated_script = response.choices[0].text
            status_code = 200
        except Exception:
            generated_script = ""
            status_code = 500

        output = GPT4ScriptGeneratorOutputDict(
            theme_text=theme_text,
            script_text=generated_script,
            component_internal_status=status_code,
        )
        return output


load_dotenv()
gpt4_script_generator_app = FastAPI()


@gpt4_script_generator_app.post("/transform/")
async def transform(
    args: GPT4ScriptGeneratorInputDict,
) -> GPT4ScriptGeneratorOutputDict:
    gpt4_script_generator = GPT4ScriptGenerator()
    return gpt4_script_generator.transform(args)

