
# Import the necessary libraries and the component
import pytest
from pydantic import ValidationError
from core.gpt4_script_generator import (
    GPT4ScriptGenerator,
    GPT4ScriptGeneratorInputDict,
    GPT4ScriptGeneratorOutputDict,
)

# Define test cases with mocked input and expected output data
test_cases = [
    (
        # Test case 1:
        GPT4ScriptGeneratorInputDict(theme_text="Write a Sci-Fi adventure"),
        GPT4ScriptGeneratorOutputDict(
            theme_text="Write a Sci-Fi adventure",
            script_text="Sample generated script for a Sci-Fi adventure",
            component_internal_status=200,
        ),
    ),
    (
        # Test case 2:
        GPT4ScriptGeneratorInputDict(theme_text="Create a romantic comedy"),
        GPT4ScriptGeneratorOutputDict(
            theme_text="Create a romantic comedy",
            script_text="Sample generated script for a romantic comedy",
            component_internal_status=200,
        ),
    ),
]

# Use @pytest.mark.parametrize to create multiple test scenarios
@pytest.mark.parametrize("input_data, expected_output", test_cases)
def test_gpt4scriptgenerator_transform(input_data, expected_output, mocker):
    # Mock the external API call to return sample data
    mocker.patch("core.gpt4_script_generator.openai.Completion.create",
                 return_value=mocker.Mock(choices=[mocker.Mock(text=expected_output.script_text)]))

    # Create the GPT4ScriptGenerator instance
    gpt4_script_generator = GPT4ScriptGenerator()

    # Call the component's transform() method with the mocked input data
    output = gpt4_script_generator.transform(input_data)

    # Assert that the output matches the expected output data
    assert output == expected_output


# Include error handling and edge case scenarios, if applicable

def test_gpt4scriptgenerator_transform_api_error(mocker):
    # Mock the external API call to raise an exception
    mocker.patch("core.gpt4_script_generator.openai.Completion.create", side_effect=Exception)

    input_data = GPT4ScriptGeneratorInputDict(theme_text="Write a mystery novel")
    
    gpt4_script_generator = GPT4ScriptGenerator()

    output = gpt4_script_generator.transform(input_data)
    
    assert output.theme_text == input_data.theme_text
    assert output.script_text == ""
    assert output.component_internal_status == 500

def test_gpt4scriptgenerator_inputdict_validation_error():
    with pytest.raises(ValidationError):
        GPT4ScriptGeneratorInputDict(theme_text=None)

def test_gpt4scriptgenerator_outputdict_validation_error():
    with pytest.raises(ValidationError):
        GPT4ScriptGeneratorOutputDict(
            theme_text="A sample theme",
            script_text=None,
            component_internal_status=500,
        )
