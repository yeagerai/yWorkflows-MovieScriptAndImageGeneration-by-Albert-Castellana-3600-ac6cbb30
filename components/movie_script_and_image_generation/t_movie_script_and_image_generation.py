
import pytest
from fastapi.testclient import TestClient
from pydantic import BaseModel
from source_code import UserInputModel, ScriptOutputModel, ImageOutputModel, movie_script_and_image_generation_app

client = TestClient(movie_script_and_image_generation_app)

test_cases = [
    # Test Case 1: Example of theme_text, script_text, and image_url
    {
        "input": UserInputModel(theme_text="example theme 1"),
        "output": {
            "script_output": ScriptOutputModel(theme_text="example theme 1", script_text="example script 1"),
            "image_output": ImageOutputModel(
                theme_text="example theme 1", script_text="example script 1", image_url="http://example.com/image1.jpg"
            ),
        },
    },
    # Test Case 2: Another example of theme_text, script_text, and image_url
    {
        "input": UserInputModel(theme_text="example theme 2"),
        "output": {
            "script_output": ScriptOutputModel(theme_text="example theme 2", script_text="example script 2"),
            "image_output": ImageOutputModel(
                theme_text="example theme 2", script_text="example script 2", image_url="http://example.com/image2.jpg"
            ),
        },
    },
]

@pytest.mark.parametrize("test_case", test_cases)
def test_transform(test_case):
    input_data = test_case["input"]
    expected_output = test_case["output"]

    # Mock the transform() method to return the expected test case output
    async def mock_transform(args: UserInputModel, callbacks: Any) -> dict:
        return test_case["output"]

    movie_script_and_image_generation_app.transform = mock_transform

    # Call the component's transform() method through the FastAPI route
    response = client.post("/transform/", json=input_data.dict())

    # Assert that the output matches the expected output
    assert response.status_code == 200
    assert response.json() == expected_output
