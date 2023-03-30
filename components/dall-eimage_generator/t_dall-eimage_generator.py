
# test_dalle_image_generator.py
import os
from unittest.mock import Mock, patch

import pytest
from fastapi.testclient import TestClient

from DALLEImageGenerator import (
    DALLEImageGenerator,
    DALLEImageGeneratorInputDict,
    DALLEImageGeneratorOutputDict,
    dalle_image_generator_app,
)

# Initialize a TestClient for testing the FastAPI app
client = TestClient(dalle_image_generator_app)

# Define mocked input and output data for test cases
input_output_data = [
    (
        DALLEImageGeneratorInputDict(script_text="Script 1", theme_text="Theme 1"),
        DALLEImageGeneratorOutputDict(
            image_url="https://example.com/image1.jpg",
            script_text="Script 1",
            theme_text="Theme 1",
        ),
    ),
    (
        DALLEImageGeneratorInputDict(script_text="Script 2", theme_text="Theme 2"),
        DALLEImageGeneratorOutputDict(
            image_url="https://example.com/image2.jpg",
            script_text="Script 2",
            theme_text="Theme 2",
        ),
    ),
]

# Test cases for the transform function using parametrize
@pytest.mark.parametrize("input_data, expected_output", input_output_data)
def test_transform(input_data, expected_output):
    with patch("requests.post") as mock_post:
        # Mock the response from the API call
        mock_response = Mock()
        mock_response.json.return_value = {
            "generated_images": [{"url": expected_output.image_url}]
        }
        mock_post.return_value = mock_response

        # Call the transform function
        dalle_image_generator = DALLEImageGenerator()
        output = dalle_image_generator.transform(input_data)

        # Check if the output matches the expected_output
        assert output == expected_output

        # Check if the API call was made with the correct parameters
        headers = {"Authorization": f"Bearer {os.environ['DALLE_API_KEY']}"}
        data = {"inputs": input_data.script_text}
        mock_post.assert_called_once_with(
            os.environ["DALLE_API_URL"], headers=headers, json=data
        )

# Test cases for the FastAPI app using parametrize
@pytest.mark.parametrize("input_data, expected_output", input_output_data)
def test_fastapi_app(input_data, expected_output):
    with patch("requests.post") as mock_post:
        # Mock the response from the API call
        mock_response = Mock()
        mock_response.json.return_value = {
            "generated_images": [{"url": expected_output.image_url}]
        }
        mock_post.return_value = mock_response

        # Call the FastAPI app
        response = client.post("/transform/", json=input_data.dict())

        # Check if the response status code is 200
        assert response.status_code == 200

        # Check if the output matches the expected_output
        output = DALLEImageGeneratorOutputDict.parse_obj(response.json())
        assert output == expected_output

        # Check if the API call was made with the correct parameters
        headers = {"Authorization": f"Bearer {os.environ['DALLE_API_KEY']}"}
        data = {"inputs": input_data.script_text}
        mock_post.assert_called_once_with(
            os.environ["DALLE_API_URL"], headers=headers, json=data
        )
