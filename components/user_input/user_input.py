
import os
from typing import Any

import yaml
from dotenv import load_dotenv
from fastapi import FastAPI
from pydantic import BaseModel

from core.abstract_component import AbstractComponent

class UserInputModel(BaseModel):
    user_text: str

class UserInputOutputDict(BaseModel):
    stored_text: str

class UserInput(AbstractComponent):
    def __init__(self) -> None:
        super().__init__()

    def transform(self, args: UserInputModel) -> UserInputOutputDict:
        print(f"Executing the transform of the {type(self).__name__} component...")
        stored_text = args.user_text
        return UserInputOutputDict(stored_text=stored_text)

load_dotenv()
user_input_app = FastAPI()

@user_input_app.post("/transform/")
async def transform(args: UserInputModel) -> Any:
    user_input = UserInput()
    return user_input.transform(args)
