
import os
from typing import Optional

import yaml
from dotenv import load_dotenv
from fastapi import FastAPI
from pydantic import BaseModel
import requests

from core.abstract_component import AbstractComponent


class DALLEImageGeneratorInputDict(BaseModel):
    script_text: str
    theme_text: str


class DALLEImageGeneratorOutputDict(BaseModel):
    image_url: str
    theme_text: str
    script_text: str


class DALLEImageGenerator(AbstractComponent):
    def __init__(self) -> None:
        super().__init__()

    def transform(
        self, args: DALLEImageGeneratorInputDict
    ) -> DALLEImageGeneratorOutputDict:
        print(f"Executing the transform of the {type(self).__name__} component...")

        # Call the DALL-E API with the received script_text and proper configuration
        # (Replace '{DALLE_API_KEY}' and '{DALLE_API_URL}' with the actual values)
        headers = {"Authorization": f"Bearer {os.environ['DALLE_API_KEY']}"}
        data = {"inputs": args.script_text}
        response = requests.post(os.environ['DALLE_API_URL'], headers=headers, json=data)

        # Parse the response and extract the image_url from the API's response
        response_data = response.json()
        image_url = response_data["generated_images"][0]["url"]

        # Store theme_text, script_text, and image_url as output
        output = DALLEImageGeneratorOutputDict(
            image_url=image_url,
            theme_text=args.theme_text,
            script_text=args.script_text
        )
        return output

load_dotenv()
dalle_image_generator_app = FastAPI()

@dalle_image_generator_app.post("/transform/")
async def transform(
    args: DALLEImageGeneratorInputDict,
) -> DALLEImageGeneratorOutputDict:
    dalle_image_generator = DALLEImageGenerator()
    return dalle_image_generator.transform(args)
