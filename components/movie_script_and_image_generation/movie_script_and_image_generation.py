
from typing import Any
from dotenv import load_dotenv
from fastapi import FastAPI
from pydantic import BaseModel

from core.workflows.abstract_workflow import AbstractWorkflow

class UserInputModel(BaseModel):
    theme_text: str

class ScriptOutputModel(BaseModel):
    theme_text: str
    script_text: str

class ImageOutputModel(BaseModel):
    theme_text: str
    script_text: str
    image_url: str

class MovieScriptAndImageGeneration(AbstractWorkflow):
    def __init__(self) -> None:
        super().__init__()

    async def transform(self, args: UserInputModel, callbacks: Any) -> None:
        results_dict = await super().transform(args=args, callbacks=callbacks)
        script_output = ScriptOutputModel(
            theme_text=args.theme_text,
            script_text=results_dict[0].script_text
        )
        image_output = ImageOutputModel(
            theme_text=args.theme_text,
            script_text=results_dict[0].script_text,
            image_url=results_dict[1].image_url
        )
        return {'script_output': script_output, 'image_output': image_output}

load_dotenv()
movie_script_and_image_generation_app = FastAPI()

@movie_script_and_image_generation_app.post("/transform/")
async def transform(args: UserInputModel) -> dict:
    movie_script_and_image_generation = MovieScriptAndImageGeneration()
    return await movie_script_and_image_generation.transform(args, callbacks=None)
