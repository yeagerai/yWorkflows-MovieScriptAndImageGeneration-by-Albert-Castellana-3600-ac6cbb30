markdown
# Component Name
GPT4ScriptGenerator

# Description
The GPT4ScriptGenerator component is a Yeager Workflow component designed to generate a script based on a given theme text by utilizing OpenAI's GPT language model. The primary function of this component is to process input data using an external API and return the generated script as output data.

# Input and Output Models
This component uses the following input and output data models:
- Input Model: `GPT4ScriptGeneratorInputDict`
    - `theme_text` (str): The theme text based on which the script will be generated.
- Output Model: `GPT4ScriptGeneratorOutputDict`
    - `theme_text` (str): The input theme text.
    - `script_text` (str): The generated script.
    - `component_internal_status` (int): The component's internal status code (200 for success, 500 for errors).

Both input and output models use Pydantic's `BaseModel` for validation and serialization.

# Parameters
- `api_key` (Optional[str]): The API key for accessing OpenAI's GPT language model. The key is retrieved from the component's configuration file.
- `model_configuration` (str): The configuration settings for the GPT language model, retrieved from the component's configuration file.

# Transform Function
The `transform()` method of the GPT4ScriptGenerator component follows these steps:
1. Set the API key for OpenAI.
2. Extract the theme text and model configuration from the input data.
3. Prepare the prompt data for the GPT language model, containing the theme and configuration data.
4. Make a request to OpenAI's Completion API with the prepared prompt.
5. If the API request is successful, extract the generated script from the API response and set the status code to 200.
6. If an error occurs during the API request, set the generated script to an empty string and set the status code to 500.
7. Create and return the output data using the GPT4ScriptGeneratorOutputDict model, containing the theme text, generated script, and status code.

# External Dependencies
The GPT4ScriptGenerator component depends on the following external libraries:
- `dotenv`: Used to load environment variables.
- `fastapi`: Used for providing a REST API endpoint.
- `openai`: Utilized to interact with OpenAI's GPT language model.
- `pydantic`: Used for input and output data validation and serialization.
- `yaml`: Used for parsing the component's configuration file.

# API Calls
The GPT4ScriptGenerator component makes API calls to OpenAI's GPT language model using the `Completion.create()` method from the `openai` library. The purpose of these calls is to generate a script based on the provided theme text and model configuration data.

# Error Handling
If an error occurs during the API call to OpenAI's GPT language model, the component catches the exception, sets the generated script to an empty string, and sets the internal status code to 500. The output data object then reflects these values, informing the user about the error status.

# Examples
To use the GPT4ScriptGenerator component within a Yeager Workflow, follow these steps:

1. Prepare the input data using the `GPT4ScriptGeneratorInputDict` model:

    