
# GPT4ScriptGenerator

This component generates a movie script using OpenAI's GPT-4 API based on the user input. It takes the 'theme_text' value from the UserInput component, sends it to GPT-4 API with an appropriate model configuration, and receives the generated script text. Then, it stores the 'theme_text' and the generated 'script_text' as output.

## Initial generation prompt
description: 'This component generates a movie script using OpenAI''s GPT-4 API based
  on the user input. It takes the ''theme_text'' value from the UserInput component,
  sends it to GPT-4 API with an appropriate model configuration, and receives the
  generated script text. Then, it stores the ''theme_text'' and the generated ''script_text''
  as output.

  '
name: GPT4ScriptGenerator


## Transformer breakdown
- Obtain the theme_text input and the model configuration
- Create the payload with the theme_text and the model configuration
- Make a request to the OpenAI GPT-4 API with the payload and the API key
- Parse the response and extract the generated script text
- Store the theme_text and generated script_text as output

## Parameters
[{'default_value': 'default', 'description': 'The model configuration for the OpenAI GPT-4 API', 'name': 'model_configuration', 'type': 'str'}, {'default_value': None, 'description': 'The API key for accessing OpenAI GPT-4 API', 'name': 'api_key', 'type': 'str'}]

        