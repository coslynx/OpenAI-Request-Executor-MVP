from fastapi.testclient import TestClient
from main import app
import pytest
import pytest_cov
import pytest_dotenv
import time
from unittest.mock import Mock

# Configure environment variables using pytest-dotenv
pytest_dotenv.load_dotenv()

# Initialize the testing client
client = TestClient(app)

@pytest.mark.asyncio
def test_create_request_success(client):
    request_text = "Write a short story about a cat"
    response = client.post("/requests/", json={"text": request_text})
    assert response.status_code == 200
    response_data = response.json()
    assert "request_id" in response_data
    assert "status" in response_data
    assert response_data["status"] == "completed"

@pytest.mark.asyncio
def test_create_request_invalid_text(client):
    request_text = "short"
    response = client.post("/requests/", json={"text": request_text})
    assert response.status_code == 400
    response_data = response.json()
    assert "detail" in response_data
    assert response_data["detail"] == "Invalid request text"

@pytest.mark.asyncio
def test_get_response_success(client):
    request_id = 123
    response = client.get(f"/responses/{request_id}")
    assert response.status_code == 200
    response_data = response.json()
    assert "response" in response_data
    assert response_data["response"] == "This is a mock response"

@pytest.mark.asyncio
def test_get_response_not_found(client):
    request_id = 999
    response = client.get(f"/responses/{request_id}")
    assert response.status_code == 404
    response_data = response.json()
    assert "detail" in response_data
    assert response_data["detail"] == "Request not found"

@pytest.fixture
def mock_openai_service(monkeypatch):
    def mock_execute_request(request_text, model="text-davinci-003"):
        return "Mock response"
    monkeypatch.setattr("services.openai_service.OpenAIService.execute_request", mock_execute_request)
    yield mock_openai_service

@pytest.mark.asyncio
def test_create_request_with_mock_openai(client, mock_openai_service):
    request_text = "Write a short story about a cat"
    response = client.post("/requests/", json={"text": request_text})
    assert response.status_code == 200
    response_data = response.json()
    assert "request_id" in response_data
    assert "status" in response_data
    assert response_data["status"] == "completed"
    mock_openai_service.execute_request.assert_called_once_with(request_text, model="text-davinci-003")

@pytest.fixture
def mock_logger(monkeypatch):
    mock_logger = Mock()
    monkeypatch.setattr("utils.logger.logger", mock_logger)
    yield mock_logger

@pytest.mark.asyncio
def test_create_request_error(client, mock_logger):
    # Simulate an error condition within `openai_service.py`
    # ... (e.g., raise an `openai.error.APIError` or an `HTTPException`)
    mock_logger.error.assert_called_once()

@pytest.mark.asyncio
def test_create_request_invalid_data(client):
    response = client.post("/requests/", json={"text": 123})
    assert response.status_code == 422
    response_data = response.json()
    assert "detail" in response_data
    assert "text" in response_data["detail"]

@pytest.mark.asyncio
def test_create_request_performance(client):
    request_text = "Write a short story about a cat"
    start_time = time.time()
    response = client.post("/requests/", json={"text": request_text})
    end_time = time.time()
    response_time = end_time - start_time
    assert response_time < 1