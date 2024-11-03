import pytest
import pytest_cov
import pytest_dotenv
from unittest.mock import Mock
import requests
import openai  # Version: 1.53.0

# Load environment variables for tests
pytest_dotenv.load_dotenv()

@pytest.fixture
def mock_openai_service(monkeypatch):
    """Mock the OpenAI service for testing."""

    def mock_execute_request(request_text, model="text-davinci-003"):
        """Mock the `execute_request` method of `OpenAIService`."""
        # Replace with your desired mocked responses based on request_text and model
        return "This is a mocked response"

    monkeypatch.setattr("services.openai_service.OpenAIService.execute_request", mock_execute_request)
    yield mock_openai_service

@pytest.mark.asyncio
def test_execute_request_success(mock_openai_service):
    """Test successful execution of a request."""
    request_text = "Write a short story about a cat"
    response = mock_openai_service.execute_request(request_text)  # Call the mocked method
    assert response == "This is a mocked response"

@pytest.mark.asyncio
def test_execute_request_invalid_text(mock_openai_service):
    """Test handling of invalid request text."""
    request_text = "short"
    with pytest.raises(ValueError) as excinfo:
        mock_openai_service.execute_request(request_text)
    assert str(excinfo.value) == "Invalid request text: Must be at least 5 characters long"

@pytest.mark.asyncio
def test_execute_request_invalid_model(mock_openai_service):
    """Test handling of an unsupported OpenAI model."""
    request_text = "Write a poem"
    model = "unsupported_model"
    with pytest.raises(ValueError) as excinfo:
        mock_openai_service.execute_request(request_text, model=model)
    assert str(excinfo.value) == f"Invalid request text or model: {model}"

@pytest.mark.asyncio
def test_execute_request_api_error(mock_openai_service, monkeypatch):
    """Test handling of an API error from OpenAI."""
    mock_response = Mock()
    mock_response.status_code = 400
    mock_response.json.return_value = {"error": "Invalid request"}

    # Mock the `openai.Completion.create` method
    monkeypatch.setattr("openai.Completion.create", Mock(side_effect=openai.error.APIError(mock_response)))

    request_text = "Write a song"
    with pytest.raises(openai.error.APIError) as excinfo:
        mock_openai_service.execute_request(request_text)
    assert excinfo.value.response.status_code == 400
    assert excinfo.value.response.json() == {"error": "Invalid request"}